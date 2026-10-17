"""
src/analytics/survival_analysis.py
Phân tích sống còn của giỏ hàng (Kaplan-Meier Estimator) và
mô hình rủi ro tỷ lệ Cox (Cox Proportional Hazards Model).
Tuân thủ: .agy/00_CORE_RULES.md và .agy/04_SURVIVAL_UPLIFT_OPTIMIZATION.md
"""

import os
import sys
import gc
import pickle
import yaml
import duckdb
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter, CoxPHFitter

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_survival_analysis():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]
    feature_store_path = config["paths"]["feature_store_path"]

    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    print("--- 1. Loading Data for Survival Analysis ---")
    con = duckdb.connect()
    df = con.execute(f"""
        SELECT 
            customer_id,
            target,
            days_since_last_session,
            days_since_last_purchase,
            cart_to_page_ratio,
            cart_abandonment_severity,
            pct_overnight_shipping,
            pct_express_shipping,
            pct_standard_shipping,
            trans_discount_usage_rate,
            bounce_rate,
            loyalty_score,
            customer_tier_code
        FROM '{feature_store_path}'
        WHERE target IS NOT NULL
    """).df()
    con.close()

    # Time-to-Event Definition:
    # Duration T: Time in days from the most recent active session / cart event.
    # Clip between 1 and 60 days to represent active consideration window.
    # Event E: 1 if converted (target == 1), 0 if right-censored (target == 0, abandoned).
    df["duration"] = np.clip(df["days_since_last_session"], 1, 60)
    df["event"] = df["target"].astype(int)

    # Primary shipping method categorization
    def assign_shipping_str(row):
        if row["pct_overnight_shipping"] > 0.4:
            return "Overnight"
        elif row["pct_express_shipping"] > 0.4:
            return "Express"
        else:
            return "Standard"

    df["shipping_category"] = df.apply(assign_shipping_str, axis=1)

    # --- 2. Kaplan-Meier Estimation ---
    print("\n--- 2. Estimating Kaplan-Meier Survival Functions ---")
    kmf_global = KaplanMeierFitter()
    kmf_global.fit(df["duration"], event_observed=df["event"], label="Tổng thể (Global)")

    # Find the golden window: Time t* where survival probability drops below 15% (or median survival)
    survival_table = kmf_global.survival_function_
    golden_cutoff_t = 14  # Default fallback
    for t_val, row in survival_table.iterrows():
        if row.iloc[0] <= 0.85:  # 15% have converted / event occurred
            golden_cutoff_t = int(t_val)
            break

    # Stratified Kaplan-Meier by Shipping Category
    kmf_strata = {}
    strata_summaries = []
    for cat in ["Standard", "Express", "Overnight"]:
        sub_df = df[df["shipping_category"] == cat]
        kmf = KaplanMeierFitter()
        kmf.fit(sub_df["duration"], event_observed=sub_df["event"], label=cat)
        kmf_strata[cat] = kmf
        
        # Calculate survival at 3, 7, 14, 30 days
        s_3d = float(kmf.predict(3))
        s_7d = float(kmf.predict(7))
        s_14d = float(kmf.predict(14))
        s_30d = float(kmf.predict(30))
        median_time = float(kmf.median_survival_time_) if not np.isinf(kmf.median_survival_time_) else 60.0

        strata_summaries.append({
            "stratum_name": f"Shipping: {cat}",
            "sample_size": len(sub_df),
            "events_observed": int(sub_df["event"].sum()),
            "survival_prob_3d": round(s_3d, 4),
            "survival_prob_7d": round(s_7d, 4),
            "survival_prob_14d": round(s_14d, 4),
            "survival_prob_30d": round(s_30d, 4),
            "median_survival_days": median_time
        })

    # Summary table
    summary_df = pd.DataFrame(strata_summaries)
    summary_csv = os.path.join(tables_dir, "tbl_ch4_survival_summary.csv")
    summary_df.to_csv(summary_csv, index=False)
    print(f"Survival summary saved to {summary_csv}:")
    print(summary_df.to_string(index=False))

    # Save KM fitters for plotting
    km_data_path = os.path.join(models_dir, "kaplan_meier_fits.pkl")
    with open(km_data_path, "wb") as f:
        pickle.dump({
            "kmf_global": kmf_global,
            "kmf_strata": kmf_strata,
            "golden_cutoff_t": golden_cutoff_t
        }, f)
    print(f"Kaplan-Meier models saved to {km_data_path}")

    # --- 3. Cox Proportional Hazards Model ---
    print("\n--- 3. Fitting Cox Proportional Hazards Model ---")
    cox_cols = [
        "duration",
        "event",
        "cart_to_page_ratio",
        "cart_abandonment_severity",
        "pct_overnight_shipping",
        "trans_discount_usage_rate",
        "bounce_rate",
        "loyalty_score"
    ]
    # Sample 30,000 for high-performance stable CoxPH inversion
    np.random.seed(42)
    sample_indices = np.random.choice(len(df), size=30000, replace=False)
    cox_df = df.iloc[sample_indices][cox_cols].dropna().copy()

    cph = CoxPHFitter(penalizer=0.01)
    cph.fit(cox_df, duration_col="duration", event_col="event")

    # Extract Hazard Ratios, CI, and p-values
    cph_summary = cph.summary.copy()
    hazard_records = []
    for var_name, row in cph_summary.iterrows():
        hr = float(np.exp(row["coef"]))
        ci_lower = float(np.exp(row["coef lower 95%"]))
        ci_upper = float(np.exp(row["coef upper 95%"]))
        p_val = float(row["p"])
        
        # Business interpretation
        if hr > 1.05 and p_val < 0.05:
            impact = "Làm tăng nguy cơ từ bỏ giỏ hàng (Rào cản ma sát)"
        elif hr < 0.95 and p_val < 0.05:
            impact = "Giảm nguy cơ từ bỏ giỏ hàng (Đòn bẩy thúc đẩy chuyển đổi)"
        else:
            impact = "Tác động trung tính / Không có ý nghĩa thống kê rõ rệt"

        hazard_records.append({
            "covariate": var_name,
            "coef": round(float(row["coef"]), 4),
            "hazard_ratio": round(hr, 4),
            "hr_lower_95": round(ci_lower, 4),
            "hr_upper_95": round(ci_upper, 4),
            "p_value": float(f"{p_val:.4e}"),
            "business_impact": impact
        })

    hr_df = pd.DataFrame(hazard_records)
    hr_csv = os.path.join(tables_dir, "tbl_ch4_coxph_hazard_ratios.csv")
    hr_df.to_csv(hr_csv, index=False)
    print(f"\nCoxPH Hazard Ratios saved to {hr_csv}:")
    print(hr_df[["covariate", "hazard_ratio", "hr_lower_95", "hr_upper_95", "p_value", "business_impact"]].to_string(index=False))

    gc.collect()


if __name__ == "__main__":
    run_survival_analysis()
