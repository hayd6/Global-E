"""
src/data_engineering/data_healing.py
Module kiểm toán và khắc phục sai lệch dữ liệu gốc (Data Healing)
Tuân thủ: .agy/00_CORE_RULES.md và .agy/01_DATA_ENGINEERING_PIT.md
"""

import os
import gc
import yaml
import duckdb
import pandas as pd


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_data_healing():
    config = load_config()
    raw_dir = config["paths"]["raw_data_dir"]
    tables_dir = config["paths"]["tables_dir"]
    processed_dir = config["paths"]["processed_data_dir"]
    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    healed_dir = os.path.join(processed_dir, "healed")
    os.makedirs(healed_dir, exist_ok=True)

    threads = config["hardware"]["threads"]
    max_memory = config["hardware"]["duckdb_max_memory"]

    con = duckdb.connect()
    con.execute(f"SET threads = {threads};")
    con.execute(f"SET max_memory = '{max_memory}';")

    audit_records = []

    # 1. Healing Customers
    print("--- Healing Customers ---")
    raw_customers_path = f"{raw_dir}/{config['raw_files']['customers']}"
    raw_cust_cnt = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{raw_customers_path}')").fetchone()[0]

    # Calculate median age per customer_tier for valid ages (18-100)
    median_ages = con.execute(f"""
        SELECT customer_tier, 
               CAST(median(CAST(age AS INT)) AS INT) as median_age
        FROM read_csv_auto('{raw_customers_path}')
        WHERE try_cast(age AS INT) IS NOT NULL 
          AND try_cast(age AS INT) >= 18 
          AND try_cast(age AS INT) <= 100
        GROUP BY customer_tier
    """).df()
    print("Median ages per customer tier:\n", median_ages)

    # Impute age, clean credit_limit, clean referral_code
    cust_healing_query = f"""
        CREATE OR REPLACE TABLE healed_customers AS
        WITH base AS (
            SELECT 
                customer_id,
                CASE 
                    WHEN try_cast(age AS INT) IS NULL OR try_cast(age AS INT) < 18 OR try_cast(age AS INT) > 100 
                    THEN NULL 
                    ELSE try_cast(age AS INT) 
                END AS raw_age,
                country_code,
                region,
                signup_date,
                CAST(loyalty_score AS FLOAT) AS loyalty_score,
                CAST(email_open_rate AS FLOAT) AS email_open_rate,
                CAST(discount_usage_rate AS FLOAT) AS discount_usage_rate,
                CAST(avg_review_score AS FLOAT) AS review_score,
                CASE WHEN referral_code IS NOT NULL AND referral_code != '' AND referral_code != '0' THEN 1 ELSE 0 END AS referral_code,
                customer_tier,
                CAST(replace(replace(credit_limit, '$', ''), ',', '') AS FLOAT) AS credit_limit,
                noise_customer_0,
                noise_customer_1,
                noise_customer_2,
                noise_customer_3,
                noise_customer_4
            FROM read_csv_auto('{raw_customers_path}')
        ),
        medians AS (
            SELECT customer_tier, CAST(median(raw_age) AS INT) as tier_median_age
            FROM base
            WHERE raw_age IS NOT NULL
            GROUP BY customer_tier
        )
        SELECT 
            b.customer_id,
            COALESCE(b.raw_age, m.tier_median_age, 35) AS age,
            b.country_code,
            b.region,
            b.signup_date,
            b.loyalty_score,
            b.email_open_rate,
            b.discount_usage_rate,
            b.review_score,
            b.referral_code,
            b.customer_tier,
            b.credit_limit,
            b.noise_customer_0,
            b.noise_customer_1,
            b.noise_customer_2,
            b.noise_customer_3,
            b.noise_customer_4
        FROM base b
        LEFT JOIN medians m ON b.customer_tier = m.customer_tier
    """
    con.execute(cust_healing_query)
    healed_cust_cnt = con.execute("SELECT COUNT(*) FROM healed_customers").fetchone()[0]
    cust_age_anomalies = con.execute(f"""
        SELECT COUNT(*) FROM read_csv_auto('{raw_customers_path}')
        WHERE try_cast(age AS INT) IS NULL OR try_cast(age AS INT) < 18 OR try_cast(age AS INT) > 100
    """).fetchone()[0]

    audit_records.append({
        "table_name": "customers",
        "raw_row_count": raw_cust_cnt,
        "healed_row_count": healed_cust_cnt,
        "anomalies_removed": cust_age_anomalies,
        "timestamp_violations_fixed": 0
    })
    con.execute(f"COPY healed_customers TO '{healed_dir}/healed_customers.parquet' (FORMAT PARQUET, COMPRESSION SNAPPY);")
    print(f"Healed customers: {healed_cust_cnt} rows saved.")

    # 2. Healing Sessions
    print("--- Healing Sessions ---")
    raw_sessions_path = f"{raw_dir}/{config['raw_files']['sessions']}"
    raw_ses_cnt = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{raw_sessions_path}')").fetchone()[0]

    # Temporal violation: session_timestamp < signup_date
    # Anomalies: pages_viewed 'N/A' or <= 0 -> 1; bounce_flag -> {0, 1}
    ses_healing_query = f"""
        CREATE OR REPLACE TABLE healed_sessions AS
        SELECT 
            s.session_id,
            s.customer_id,
            s.session_timestamp,
            CAST(s.session_duration AS FLOAT) AS session_duration,
            CASE 
                WHEN try_cast(s.pages_viewed AS INT) IS NULL OR try_cast(s.pages_viewed AS INT) <= 0 
                THEN 1 
                ELSE try_cast(s.pages_viewed AS INT) 
            END AS pages_viewed,
            s.cart_additions,
            CASE 
                WHEN lower(cast(s.bounce_flag as varchar)) IN ('1', 'true', 'yes') THEN 1 
                ELSE 0 
            END AS bounce_flag,
            s.traffic_source,
            s.device_type,
            s.campaign_id,
            s.geo_ip_region
        FROM read_csv_auto('{raw_sessions_path}') s
        JOIN healed_customers c ON s.customer_id = c.customer_id
        WHERE s.session_timestamp >= c.signup_date
    """
    con.execute(ses_healing_query)
    healed_ses_cnt = con.execute("SELECT COUNT(*) FROM healed_sessions").fetchone()[0]
    ses_time_violations = raw_ses_cnt - healed_ses_cnt
    ses_page_anomalies = con.execute(f"""
        SELECT COUNT(*) FROM read_csv_auto('{raw_sessions_path}')
        WHERE try_cast(pages_viewed AS INT) IS NULL OR try_cast(pages_viewed AS INT) <= 0
    """).fetchone()[0]

    audit_records.append({
        "table_name": "sessions",
        "raw_row_count": raw_ses_cnt,
        "healed_row_count": healed_ses_cnt,
        "anomalies_removed": ses_page_anomalies,
        "timestamp_violations_fixed": ses_time_violations
    })
    con.execute(f"COPY healed_sessions TO '{healed_dir}/healed_sessions.parquet' (FORMAT PARQUET, COMPRESSION SNAPPY);")
    print(f"Healed sessions: {healed_ses_cnt} rows saved (removed {ses_time_violations} violations).")

    # 3. Healing Transactions
    print("--- Healing Transactions ---")
    raw_trans_path = f"{raw_dir}/{config['raw_files']['transactions']}"
    raw_tx_cnt = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{raw_trans_path}')").fetchone()[0]

    tx_healing_query = f"""
        CREATE OR REPLACE TABLE healed_transactions AS
        SELECT 
            t.transaction_id,
            t.customer_id,
            t.transaction_timestamp,
            CAST(replace(replace(t.order_value, '$', ''), ',', '') AS DOUBLE) AS order_value,
            t.items_count,
            t.payment_method,
            CASE 
                WHEN lower(cast(t.discount_applied as varchar)) IN ('1', 'true', 'yes') THEN 1 
                ELSE 0 
            END AS discount_applied,
            lower(t.shipping_speed) AS shipping_speed,
            t.high_value_flag,
            t.noise_trans_0,
            t.noise_trans_1
        FROM read_csv_auto('{raw_trans_path}') t
        JOIN healed_customers c ON t.customer_id = c.customer_id
        WHERE t.transaction_timestamp >= c.signup_date
          AND NOT (t.items_count <= 0 AND try_cast(replace(replace(t.order_value, '$', ''), ',', '') AS DOUBLE) > 0)
    """
    con.execute(tx_healing_query)
    healed_tx_cnt = con.execute("SELECT COUNT(*) FROM healed_transactions").fetchone()[0]

    tx_bad_items = con.execute(f"""
        SELECT COUNT(*) FROM read_csv_auto('{raw_trans_path}')
        WHERE items_count <= 0 AND try_cast(replace(replace(order_value, '$', ''), ',', '') AS DOUBLE) > 0
    """).fetchone()[0]
    tx_time_violations = con.execute(f"""
        SELECT COUNT(*) FROM read_csv_auto('{raw_trans_path}') t
        JOIN healed_customers c ON t.customer_id = c.customer_id
        WHERE t.transaction_timestamp < c.signup_date
    """).fetchone()[0]

    audit_records.append({
        "table_name": "transactions",
        "raw_row_count": raw_tx_cnt,
        "healed_row_count": healed_tx_cnt,
        "anomalies_removed": tx_bad_items,
        "timestamp_violations_fixed": tx_time_violations
    })
    con.execute(f"COPY healed_transactions TO '{healed_dir}/healed_transactions.parquet' (FORMAT PARQUET, COMPRESSION SNAPPY);")
    print(f"Healed transactions: {healed_tx_cnt} rows saved (removed {raw_tx_cnt - healed_tx_cnt} total anomalies/violations).")

    # 4. Other tables (campaigns, geo_data, train, test, sample_submission)
    other_tables = [
        ("marketing_campaigns", config["raw_files"]["campaigns"]),
        ("geo_data", config["raw_files"]["geo_data"]),
        ("train", config["raw_files"]["train"]),
        ("test", config["raw_files"]["test"]),
        ("sample_submission", config["raw_files"]["sample_submission"])
    ]
    for tbl_name, fname in other_tables:
        fpath = f"{raw_dir}/{fname}"
        cnt = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{fpath}')").fetchone()[0]
        audit_records.append({
            "table_name": tbl_name,
            "raw_row_count": cnt,
            "healed_row_count": cnt,
            "anomalies_removed": 0,
            "timestamp_violations_fixed": 0
        })

    # Save audit table
    audit_df = pd.DataFrame(audit_records)
    audit_csv_path = os.path.join(tables_dir, "tbl_ch1_data_healing_audit.csv")
    audit_df.to_csv(audit_csv_path, index=False)
    print(f"\nAudit table successfully exported to {audit_csv_path}:")
    print(audit_df.to_string(index=False))

    con.close()
    gc.collect()


if __name__ == "__main__":
    run_data_healing()
