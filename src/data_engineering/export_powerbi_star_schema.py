"""
src/data_engineering/export_powerbi_star_schema.py
Kết xuất 4 bảng Star Schema chuẩn hóa cho Power BI:
1. fact_customer_decisions.csv (200,000 dòng)
2. dim_customers.csv (200,000 dòng)
3. dim_cart_behavior.csv (200,000 dòng)
4. dim_threshold_simulation.csv (100 dòng)
Tuân thủ: .agy/00_CORE_RULES.md và .agy/05_DASHBOARD_WEB_AND_REPORT.md
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import gc
import pickle
import yaml
import duckdb
import numpy as np
import pandas as pd
from src.models.pipeline_wrapper import FullPipelineModel

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def export_star_schema():
    config = load_config()
    powerbi_dir = config["paths"]["powerbi_dir"]
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]
    processed_dir = config["paths"]["processed_data_dir"]
    raw_dir = config["paths"]["raw_data_dir"]
    feature_store_path = config["paths"]["feature_store_path"]

    os.makedirs(powerbi_dir, exist_ok=True)

    threads = config["hardware"]["threads"]
    max_memory = config["hardware"]["duckdb_max_memory"]

    con = duckdb.connect()
    con.execute(f"SET threads = {threads};")
    con.execute(f"SET max_memory = '{max_memory}';")

    print("--- 1. Generating Model Predictions on Full Population (200,000) ---")
    with open(os.path.join(models_dir, "best_calibrated_model.pkl"), "rb") as f:
        best_model = pickle.load(f)

    # Read optimal tau from threshold optimization
    thresh_csv = os.path.join(tables_dir, "tbl_ch5_threshold_optimization_results.csv")
    thresh_df = pd.read_csv(thresh_csv)
    optimal_tau = float(thresh_df.sort_values("expected_net_profit_usd", ascending=False).iloc[0]["threshold"])
    print(f"Optimal Decision Threshold tau*: {optimal_tau:.2f}")

    # Load all 200,000 customer features
    print("Reading PIT features...")
    full_pit_df = con.execute(f"""
        SELECT * EXCLUDE (target)
        FROM '{feature_store_path}'
        ORDER BY customer_id
    """).df()

    targets_df = con.execute(f"""
        SELECT customer_id, target
        FROM '{feature_store_path}'
        ORDER BY customer_id
    """).df()

    # Predict calibrated probability
    print("Computing calibrated probabilities for all 200,000 customers...")
    p_all = best_model.predict_proba(full_pit_df.drop(columns=["customer_id"]))[:, 1].astype(np.float32)

    # Assign decile ranks (1 = top 10% highest probability, 10 = lowest)
    decile_ranks = pd.qcut(-p_all, q=10, labels=list(range(1, 11))).astype(int)

    # Decisions at optimal tau*
    decisions = (p_all >= optimal_tau).astype(np.int8)

    # Calculate CLV / AOV proxy and Expected Profit
    valid_aov_median = 85.0
    aov_series = np.where(full_pit_df["avg_order_value"] > 0, full_pit_df["avg_order_value"], valid_aov_median)
    margin_series = 0.25 * aov_series

    # Convert target_vals to standard numpy float array with np.nan for missing
    c_contact = 1.0
    c_voucher = 5.0
    target_clean = targets_df["target"].astype(float).to_numpy()
    effective_y = np.where(np.isnan(target_clean), p_all, target_clean)
    net_profit_series = (decisions * (effective_y * (margin_series - c_voucher) - c_contact)).astype(np.float32)

    # Load GMM assignments and Uplift scores
    assign_path = os.path.join(processed_dir, "customer_cluster_assignments.parquet")
    uplift_path = os.path.join(processed_dir, "customer_uplift_scores.parquet")

    gmm_df = con.execute(f"SELECT customer_id, gmm_cluster_id FROM '{assign_path}' ORDER BY customer_id").df()
    uplift_df = con.execute(f"SELECT customer_id, uplift_score, uplift_segment FROM '{uplift_path}' ORDER BY customer_id").df()

    # --- 2. Bảng Fact: fact_customer_decisions.csv (200,000 dòng) ---
    print("\n--- 2. Exporting Fact Table: fact_customer_decisions.csv ---")
    fact_df = pd.DataFrame({
        "customer_id": full_pit_df["customer_id"],
        "target_actual": targets_df["target"],  # contains 0, 1, or NaN
        "predicted_prob_calibrated": np.round(p_all, 4),
        "decision_optimal_tau": decisions,
        "uplift_score": np.round(uplift_df["uplift_score"].values, 4),
        "uplift_segment": uplift_df["uplift_segment"].values,
        "gmm_cluster_id": gmm_df["gmm_cluster_id"].values,
        "clv_predicted_usd": np.round(aov_series, 2),
        "expected_margin_usd": np.round(margin_series, 2),
        "expected_net_profit_usd": np.round(net_profit_series, 2),
        "decile_rank": decile_ranks
    })

    fact_csv = os.path.join(powerbi_dir, "fact_customer_decisions.csv")
    fact_df.to_csv(fact_csv, index=False)
    print(f"Fact table saved to {fact_csv} ({len(fact_df):,} rows)")

    # --- 3. Bảng Chiều khách hàng: dim_customers.csv (200,000 dòng) ---
    print("\n--- 3. Exporting Dimension Table: dim_customers.csv ---")
    raw_cust_path = f"{raw_dir}/{config['raw_files']['customers']}"
    healed_cust_path = f"{processed_dir}/healed/healed_customers.parquet"

    # Define age groups
    def get_age_group(age):
        if age < 25:
            return "<25"
        elif age <= 34:
            return "25-34"
        elif age <= 44:
            return "35-44"
        elif age <= 54:
            return "45-54"
        else:
            return "55+"

    # Define credit limit tiers
    def get_credit_tier(cred):
        if cred < 3000:
            return "Low"
        elif cred < 7000:
            return "Medium"
        elif cred < 15000:
            return "High"
        else:
            return "VIP"

    dim_cust_df = con.execute(f"""
        SELECT 
            c.customer_id,
            c.age,
            c.country_code AS country,
            c.signup_date AS registration_date,
            c.customer_tier,
            c.loyalty_score,
            c.credit_limit
        FROM '{healed_cust_path}' c
        ORDER BY c.customer_id
    """).df()

    dim_cust_df["age_group"] = dim_cust_df["age"].apply(get_age_group)
    dim_cust_df["credit_limit_tier"] = dim_cust_df["credit_limit"].apply(get_credit_tier)
    dim_cust_df["gender"] = "Unknown"  # Standard neutral gender category

    # Reorder columns as specified in DATA DICTIONARY
    dim_cust_final = dim_cust_df[[
        "customer_id",
        "age",
        "age_group",
        "gender",
        "country",
        "registration_date",
        "customer_tier",
        "loyalty_score",
        "credit_limit",
        "credit_limit_tier"
    ]]
    dim_cust_csv = os.path.join(powerbi_dir, "dim_customers.csv")
    dim_cust_final.to_csv(dim_cust_csv, index=False)
    print(f"Dimension customers saved to {dim_cust_csv} ({len(dim_cust_final):,} rows)")

    # --- 4. Bảng Chiều hành vi giỏ hàng: dim_cart_behavior.csv (200,000 dòng) ---
    print("\n--- 4. Exporting Dimension Table: dim_cart_behavior.csv ---")
    def get_risk_level(severity):
        if severity == 0:
            return "Low"
        elif severity <= 2:
            return "Medium"
        elif severity <= 5:
            return "High"
        else:
            return "Severe"

    dim_cart_df = pd.DataFrame({
        "customer_id": full_pit_df["customer_id"],
        "total_sessions": full_pit_df["total_sessions"],
        "total_pages_viewed": full_pit_df["total_pages_viewed"],
        "total_cart_additions": full_pit_df["total_cart_additions"],
        "cart_to_page_ratio": np.round(full_pit_df["cart_to_page_ratio"], 4),
        "cart_abandonment_severity": full_pit_df["cart_abandonment_severity"],
        "cart_velocity": np.round(full_pit_df["cart_velocity"], 4),
        "hesitation_index": np.round(full_pit_df["hesitation_index"], 2),
        "days_since_last_session": full_pit_df["days_since_last_session"],
        "bounce_rate": np.round(full_pit_df["bounce_rate"], 4),
        "pct_overnight_shipping": np.round(full_pit_df["pct_overnight_shipping"], 4),
        "abandonment_risk_level": full_pit_df["cart_abandonment_severity"].apply(get_risk_level)
    })
    dim_cart_csv = os.path.join(powerbi_dir, "dim_cart_behavior.csv")
    dim_cart_df.to_csv(dim_cart_csv, index=False)
    print(f"Dimension cart behavior saved to {dim_cart_csv} ({len(dim_cart_df):,} rows)")

    # --- 5. Bảng Chiều mô phỏng tài chính: dim_threshold_simulation.csv (100 dòng) ---
    print("\n--- 5. Exporting Simulation Table: dim_threshold_simulation.csv ---")
    sim_source_csv = os.path.join(tables_dir, "tbl_ch5_threshold_optimization_results.csv")
    sim_df = pd.read_csv(sim_source_csv)
    dim_sim_csv = os.path.join(powerbi_dir, "dim_threshold_simulation.csv")
    sim_df.to_csv(dim_sim_csv, index=False)
    print(f"Simulation dimension saved to {dim_sim_csv} ({len(sim_df):,} rows)")

    con.close()
    gc.collect()


if __name__ == "__main__":
    export_star_schema()
