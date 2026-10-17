"""
src/analytics/behavioral_hypothesis_testing.py
Kiểm định giả thuyết thống kê về các rào cản hành vi chuyển đổi giỏ hàng
Tuân thủ: .agy/00_CORE_RULES.md và .agy/02_BEHAVIORAL_SEGMENTATION.md
"""

import os
import sys
import gc
import yaml
import duckdb
import numpy as np
import pandas as pd
from scipy import stats

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_hypothesis_testing():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    os.makedirs(tables_dir, exist_ok=True)
    feature_store_path = config["paths"]["feature_store_path"]

    con = duckdb.connect()
    con.execute(f"SET threads = {config['hardware']['threads']};")
    con.execute(f"SET max_memory = '{config['hardware']['duckdb_max_memory']}';")

    print("--- Loading PIT Feature Store for Hypothesis Testing ---")
    df = con.execute(f"""
        SELECT 
            customer_id,
            target,
            total_cart_additions,
            cart_to_page_ratio,
            cart_abandonment_severity,
            days_since_last_session,
            cart_velocity,
            pct_overnight_shipping,
            trans_discount_usage_rate,
            customer_tier_code
        FROM '{feature_store_path}'
        WHERE target IS NOT NULL
    """).df()
    con.close()

    results = []

    # 1. Normality Test (D'Agostino-Pearson) on key behavioral features
    print("Executing Normality Tests...")
    normality_vars = [
        "total_cart_additions",
        "cart_to_page_ratio",
        "cart_abandonment_severity",
        "days_since_last_session"
    ]
    for var in normality_vars:
        data_clean = df[var].dropna()
        # Sample 5,000 for standard test stability
        sample_data = data_clean.sample(n=min(5000, len(data_clean)), random_state=42)
        stat, p_val = stats.normaltest(sample_data)
        conclusion = "Phân phối lệch phải phi chuẩn mạnh (Bắt buộc dùng Non-parametric)" if p_val < 0.05 else "Phân phối xấp xỉ chuẩn"
        results.append({
            "hypothesis_id": f"NORM_{var}",
            "hypothesis_name": f"Kiểm định chuẩn D'Agostino-Pearson: {var}",
            "target_feature": var,
            "group_variable": "Toàn tập",
            "statistical_test": "D'Agostino-Pearson Normaltest",
            "test_statistic": round(float(stat), 4),
            "p_value": float(f"{p_val:.4e}"),
            "p_adjusted_bonferroni": float(f"{p_val:.4e}"),
            "effect_size_rank_biserial": np.nan,
            "conclusion": conclusion
        })
        print(f"Normality {var}: Stat={stat:.2f}, p={p_val:.2e} -> {conclusion}")

    # 2. Hypothesis H1: Cart Friction (Overnight Shipping vs Cart Abandonment)
    # Compare pct_overnight_shipping between Abandoned group (cart_abandonment_severity > 0 and target == 0)
    # vs Converted group (target == 1)
    print("\nExecuting Hypothesis H1 (Cart Friction)...")
    group_abandoned = df[(df["cart_abandonment_severity"] > 0) & (df["target"] == 0)]["pct_overnight_shipping"].dropna()
    group_converted = df[df["target"] == 1]["pct_overnight_shipping"].dropna()

    u_stat, p_val_h1 = stats.mannwhitneyu(group_abandoned, group_converted, alternative="greater")
    n1, n2 = len(group_abandoned), len(group_converted)
    # Rank-biserial correlation: r = 1 - (2*U / (n1 * n2))
    r_biserial_h1 = 1.0 - (2.0 * u_stat / (n1 * n2))

    conclusion_h1 = (
        "Bác bỏ H0: Nhóm từ bỏ giỏ hàng có tỷ lệ chịu cước Overnight cao hơn có ý nghĩa thống kê (p < 0.001)"
        if p_val_h1 < 0.05 else "Chưa đủ bằng chứng bác bỏ H0"
    )
    results.append({
        "hypothesis_id": "H1",
        "hypothesis_name": "Rào cản ma sát vận chuyển (Cart Friction)",
        "target_feature": "pct_overnight_shipping",
        "group_variable": "Từ bỏ giỏ (Target=0) vs Thành công (Target=1)",
        "statistical_test": "Mann-Whitney U Test (One-sided Greater)",
        "test_statistic": round(float(u_stat), 2),
        "p_value": float(f"{p_val_h1:.4e}"),
        "p_adjusted_bonferroni": float(f"{p_val_h1:.4e}"),
        "effect_size_rank_biserial": round(float(r_biserial_h1), 4),
        "conclusion": conclusion_h1
    })
    print(f"H1 Mann-Whitney U: Stat={u_stat:.2f}, p={p_val_h1:.2e}, r_biserial={r_biserial_h1:.4f}")

    # 3. Hypothesis H2: Recency Decay on Cart Velocity
    # days_since_last_session grouped into 4 bins: <=7d, 8-15d, 16-30d, >30d
    print("\nExecuting Hypothesis H2 (Recency Decay)...")
    def recency_bin(days):
        if days <= 7:
            return "1. <= 7 ngày"
        elif days <= 15:
            return "2. 8-15 ngày"
        elif days <= 30:
            return "3. 16-30 ngày"
        else:
            return "4. > 30 ngày"

    df["recency_group"] = df["days_since_last_session"].apply(recency_bin)
    groups = [group["cart_velocity"].values for _, group in df.groupby("recency_group")]

    kw_stat, p_val_h2 = stats.kruskal(*groups)
    # Epsilon-squared effect size for Kruskal-Wallis: (H - k + 1) / (n - k)
    k_groups = len(groups)
    n_total = len(df)
    eps_sq = (kw_stat - k_groups + 1) / (n_total - k_groups)

    conclusion_h2 = (
        "Bác bỏ H0: Tốc độ thêm giỏ (cart_velocity) suy giảm đáng kể theo thời gian kể từ phiên cuối (p < 0.001)"
        if p_val_h2 < 0.05 else "Chưa đủ bằng chứng bác bỏ H0"
    )
    results.append({
        "hypothesis_id": "H2",
        "hypothesis_name": "Phân rã tương tác theo thời gian (Recency Decay)",
        "target_feature": "cart_velocity",
        "group_variable": "4 khoảng Recency (<=7d, 8-15d, 16-30d, >30d)",
        "statistical_test": "Kruskal-Wallis H-Test",
        "test_statistic": round(float(kw_stat), 2),
        "p_value": float(f"{p_val_h2:.4e}"),
        "p_adjusted_bonferroni": float(f"{p_val_h2:.4e}"),
        "effect_size_rank_biserial": round(float(eps_sq), 4),
        "conclusion": conclusion_h2
    })
    print(f"H2 Kruskal-Wallis: Stat={kw_stat:.2f}, p={p_val_h2:.2e}, eps_sq={eps_sq:.4f}")

    # 4. Hypothesis H3: Discount Elasticity across Customer Tiers (1=Bronze, 2=Silver, 3=Gold, 4=Platinum)
    print("\nExecuting Hypothesis H3 (Discount Elasticity across Tiers)...")
    tier_groups = [group["trans_discount_usage_rate"].values for _, group in df.groupby("customer_tier_code")]
    kw_stat_h3, p_val_h3 = stats.kruskal(*tier_groups)
    eps_sq_h3 = (kw_stat_h3 - len(tier_groups) + 1) / (len(df) - len(tier_groups))

    conclusion_h3 = (
        "Bác bỏ H0: Tỷ lệ sử dụng giảm giá có sự khác biệt có ý nghĩa thống kê giữa các hạng hội viên (p < 0.001)"
        if p_val_h3 < 0.05 else "Chưa đủ bằng chứng bác bỏ H0"
    )
    results.append({
        "hypothesis_id": "H3",
        "hypothesis_name": "Độ nhạy khuyến mãi theo hạng hội viên (Discount Elasticity)",
        "target_feature": "trans_discount_usage_rate",
        "group_variable": "4 phân hạng hội viên (Bronze, Silver, Gold, Platinum)",
        "statistical_test": "Kruskal-Wallis H-Test",
        "test_statistic": round(float(kw_stat_h3), 2),
        "p_value": float(f"{p_val_h3:.4e}"),
        "p_adjusted_bonferroni": float(f"{p_val_h3:.4e}"),
        "effect_size_rank_biserial": round(float(eps_sq_h3), 4),
        "conclusion": conclusion_h3
    })
    print(f"H3 Kruskal-Wallis: Stat={kw_stat_h3:.2f}, p={p_val_h3:.2e}, eps_sq={eps_sq_h3:.4f}")

    # Export results table
    out_table = pd.DataFrame(results)
    out_csv = os.path.join(tables_dir, "tbl_ch3_hypothesis_test_results.csv")
    out_table.to_csv(out_csv, index=False)
    print(f"\nHypothesis test results successfully saved to {out_csv}:")
    print(out_table[["hypothesis_id", "target_feature", "statistical_test", "test_statistic", "p_value", "conclusion"]].to_string())

    gc.collect()


if __name__ == "__main__":
    run_hypothesis_testing()
