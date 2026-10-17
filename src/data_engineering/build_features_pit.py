"""
src/data_engineering/build_features_pit.py
Trích xuất Feature Store Point-in-Time (PIT) cấp khách hàng (1 dòng = 1 khách hàng)
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


def build_features_pit():
    config = load_config()
    raw_dir = config["paths"]["raw_data_dir"]
    processed_dir = config["paths"]["processed_data_dir"]
    tables_dir = config["paths"]["tables_dir"]
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)

    healed_dir = os.path.join(processed_dir, "healed")
    cutoff_date = config["point_in_time"]["cutoff_date"]
    threads = config["hardware"]["threads"]
    max_memory = config["hardware"]["duckdb_max_memory"]

    output_parquet = config["paths"]["feature_store_path"]
    sample_csv = os.path.join(tables_dir, "customer_features_pit_sample.csv")
    dictionary_csv = os.path.join(tables_dir, "tbl_ch3_feature_dictionary.csv")

    con = duckdb.connect()
    con.execute(f"SET threads = {threads};")
    con.execute(f"SET max_memory = '{max_memory}';")

    print(f"--- Building PIT Feature Store at Cutoff: {cutoff_date} ---")

    # Step 1: Sessions aggregation <= cutoff_date
    print("Aggregating sessions <= cutoff_date...")
    session_agg_query = f"""
        CREATE OR REPLACE TABLE agg_sessions AS
        WITH ses_filtered AS (
            SELECT 
                s.session_id,
                s.customer_id,
                s.session_timestamp,
                s.session_duration,
                s.pages_viewed,
                s.cart_additions,
                s.bounce_flag,
                s.traffic_source,
                s.device_type,
                s.campaign_id,
                s.geo_ip_region,
                -- Check if there was any transaction by this customer on the session date
                CASE 
                    WHEN s.cart_additions > 0 AND tx.customer_id IS NULL THEN 1 
                    ELSE 0 
                END AS is_cart_abandoned
            FROM '{healed_dir}/healed_sessions.parquet' s
            LEFT JOIN (
                SELECT DISTINCT customer_id, transaction_timestamp
                FROM '{healed_dir}/healed_transactions.parquet'
                WHERE transaction_timestamp <= '{cutoff_date}'
            ) tx ON s.customer_id = tx.customer_id AND s.session_timestamp = tx.transaction_timestamp
            WHERE s.session_timestamp <= '{cutoff_date}'
        ),
        ses_metrics AS (
            SELECT 
                customer_id,
                COUNT(*) AS total_sessions,
                SUM(session_duration) AS total_duration_sec,
                AVG(session_duration) AS avg_session_duration,
                SUM(pages_viewed) AS total_pages_viewed,
                AVG(pages_viewed) AS avg_pages_per_session,
                AVG(bounce_flag) AS bounce_rate,
                DATE_DIFF('day', MAX(session_timestamp), CAST('{cutoff_date}' AS DATE)) AS days_since_last_session,
                
                -- Activity trend slope: sessions in [t0-15d, t0] vs [t0-30d, t0-15d]
                COUNT(CASE WHEN session_timestamp >= CAST('{cutoff_date}' AS DATE) - INTERVAL 15 DAY THEN 1 END) AS ses_last_15d,
                COUNT(CASE WHEN session_timestamp >= CAST('{cutoff_date}' AS DATE) - INTERVAL 30 DAY AND session_timestamp < CAST('{cutoff_date}' AS DATE) - INTERVAL 15 DAY THEN 1 END) AS ses_prev_15d,
                
                -- Cart barriers
                SUM(cart_additions) AS total_cart_additions,
                SUM(is_cart_abandoned) AS cart_abandonment_severity,
                COUNT(CASE WHEN cart_additions > 0 THEN 1 END) AS cart_sessions_count,
                
                -- Device shares
                COUNT(CASE WHEN lower(device_type) = 'mobile' THEN 1 END) AS mobile_sessions,
                COUNT(CASE WHEN lower(device_type) = 'desktop' THEN 1 END) AS desktop_sessions,
                COUNT(CASE WHEN lower(device_type) = 'tablet' THEN 1 END) AS tablet_sessions,
                
                -- Traffic source shares
                COUNT(CASE WHEN campaign_id IS NOT NULL AND campaign_id > 0 THEN 1 END) AS campaign_sessions,
                COUNT(CASE WHEN lower(traffic_source) = 'direct' THEN 1 END) AS direct_sessions,
                COUNT(CASE WHEN lower(traffic_source) = 'organic' THEN 1 END) AS organic_sessions,
                COUNT(CASE WHEN lower(traffic_source) = 'paid search' THEN 1 END) AS paid_sessions,
                
                -- Primary geo region for customer
                MODE(geo_ip_region) AS primary_geo_region
            FROM ses_filtered
            GROUP BY customer_id
        )
        SELECT 
            customer_id,
            total_sessions,
            total_duration_sec,
            avg_session_duration,
            total_pages_viewed,
            avg_pages_per_session,
            bounce_rate,
            days_since_last_session,
            CAST(ses_last_15d * 1.0 / (ses_prev_15d + 1.0) AS FLOAT) AS activity_trend_slope,
            total_cart_additions,
            cart_abandonment_severity,
            cart_sessions_count,
            CAST(mobile_sessions * 1.0 / total_sessions AS FLOAT) AS pct_mobile_sessions,
            CAST(desktop_sessions * 1.0 / total_sessions AS FLOAT) AS pct_desktop_sessions,
            CAST(tablet_sessions * 1.0 / total_sessions AS FLOAT) AS pct_tablet_sessions,
            CAST(campaign_sessions * 1.0 / total_sessions AS FLOAT) AS pct_campaign_sessions,
            CAST(direct_sessions * 1.0 / total_sessions AS FLOAT) AS traffic_source_direct_ratio,
            CAST(organic_sessions * 1.0 / total_sessions AS FLOAT) AS traffic_source_organic_ratio,
            CAST(paid_sessions * 1.0 / total_sessions AS FLOAT) AS traffic_source_paid_ratio,
            primary_geo_region
        FROM ses_metrics
    """
    con.execute(session_agg_query)
    print("Session metrics table created.")

    # Step 2: Transactions aggregation <= cutoff_date
    print("Aggregating transactions <= cutoff_date...")
    tx_agg_query = f"""
        CREATE OR REPLACE TABLE agg_transactions AS
        SELECT 
            customer_id,
            COUNT(*) AS trans_count,
            SUM(order_value) AS total_spend,
            AVG(order_value) AS avg_order_value,
            MAX(order_value) AS max_order_value,
            MIN(order_value) AS min_order_value,
            SUM(items_count) AS total_items_purchased,
            AVG(items_count) AS items_per_trans,
            DATE_DIFF('day', MAX(transaction_timestamp), CAST('{cutoff_date}' AS DATE)) AS days_since_last_purchase,
            AVG(discount_applied) AS trans_discount_usage_rate,
            CAST(COUNT(CASE WHEN shipping_speed = 'overnight' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_overnight_shipping,
            CAST(COUNT(CASE WHEN shipping_speed = 'express' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_express_shipping,
            CAST(COUNT(CASE WHEN shipping_speed = 'standard' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_standard_shipping,
            CAST(COUNT(CASE WHEN high_value_flag = true THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS high_value_trans_ratio
        FROM '{healed_dir}/healed_transactions.parquet'
        WHERE transaction_timestamp <= '{cutoff_date}'
        GROUP BY customer_id
    """
    con.execute(tx_agg_query)
    print("Transaction metrics table created.")

    # Step 3: Combine with customers, geo_data, and train/test labels
    print("Joining feature tables and engineering ratios...")
    geo_path = f"{raw_dir}/{config['raw_files']['geo_data']}"
    train_path = f"{raw_dir}/{config['raw_files']['train']}"

    feature_store_query = f"""
        CREATE OR REPLACE TABLE customer_features_pit AS
        SELECT 
            c.customer_id,
            
            -- Demographics & Account
            CAST(c.age AS INT) AS age,
            CAST(DATE_DIFF('day', c.signup_date, CAST('{cutoff_date}' AS DATE)) AS INT) AS account_age_days,
            CAST(CASE 
                WHEN lower(c.customer_tier) = 'bronze' THEN 1
                WHEN lower(c.customer_tier) = 'silver' THEN 2
                WHEN lower(c.customer_tier) = 'gold' THEN 3
                WHEN lower(c.customer_tier) = 'platinum' THEN 4
                ELSE 1 
            END AS TINYINT) AS customer_tier_code,
            CAST(c.loyalty_score AS FLOAT) AS loyalty_score,
            CAST(c.credit_limit AS FLOAT) AS credit_limit,
            CAST(c.email_open_rate AS FLOAT) AS email_open_rate,
            CAST(c.discount_usage_rate AS FLOAT) AS discount_usage_rate_cust,
            CAST(c.review_score AS FLOAT) AS review_score,
            CAST(c.referral_code AS TINYINT) AS referral_code,
            
            -- Engagement metrics
            CAST(COALESCE(s.total_sessions, 0) AS INT) AS total_sessions,
            CAST(COALESCE(s.total_duration_sec, 0.0) AS FLOAT) AS total_duration_sec,
            CAST(COALESCE(s.avg_session_duration, 0.0) AS FLOAT) AS avg_session_duration,
            CAST(COALESCE(s.total_pages_viewed, 0) AS INT) AS total_pages_viewed,
            CAST(COALESCE(s.avg_pages_per_session, 0.0) AS FLOAT) AS avg_pages_per_session,
            CAST(COALESCE(s.bounce_rate, 0.0) AS FLOAT) AS bounce_rate,
            CAST(COALESCE(s.days_since_last_session, 999) AS INT) AS days_since_last_session,
            CAST(COALESCE(s.activity_trend_slope, 1.0) AS FLOAT) AS activity_trend_slope,
            CAST(COALESCE(s.total_sessions, 0) * 1.0 / (DATE_DIFF('day', c.signup_date, CAST('{cutoff_date}' AS DATE)) / 30.0 + 1.0) AS FLOAT) AS session_frequency_per_month,
            
            -- Cart barrier & friction metrics
            CAST(COALESCE(s.total_cart_additions, 0) AS INT) AS total_cart_additions,
            CAST(COALESCE(s.total_cart_additions, 0) * 1.0 / (COALESCE(s.total_pages_viewed, 0) + 1.0) AS FLOAT) AS cart_to_page_ratio,
            CAST(COALESCE(s.total_cart_additions, 0) * 1.0 / (COALESCE(s.total_sessions, 0) + 1.0) AS FLOAT) AS cart_velocity,
            CAST(COALESCE(s.cart_abandonment_severity, 0) AS INT) AS cart_abandonment_severity,
            CAST(COALESCE(s.cart_abandonment_severity, 0) * 1.0 / (COALESCE(s.total_sessions, 0) + 1.0) AS FLOAT) AS abandonment_ratio,
            CAST(COALESCE(s.total_duration_sec, 0.0) / (COALESCE(s.total_cart_additions, 0) + 1.0) AS FLOAT) AS hesitation_index,
            CAST((COALESCE(s.total_duration_sec, 0.0) / (COALESCE(s.total_cart_additions, 0) + 1.0)) / (COALESCE(s.avg_session_duration, 0.0) + 1.0) AS FLOAT) AS cart_hesitation_ratio,
            CAST(COALESCE(s.cart_sessions_count, 0) * 1.0 / (COALESCE(s.total_sessions, 0) + 1.0) AS FLOAT) AS cart_sessions_ratio,
            
            -- Transactions & spend metrics
            CAST(COALESCE(t.trans_count, 0) AS INT) AS trans_count,
            CAST(COALESCE(t.total_spend, 0.0) AS FLOAT) AS total_spend,
            CAST(COALESCE(t.avg_order_value, 0.0) AS FLOAT) AS avg_order_value,
            CAST(COALESCE(t.max_order_value, 0.0) AS FLOAT) AS max_order_value,
            CAST(COALESCE(t.min_order_value, 0.0) AS FLOAT) AS min_order_value,
            CAST(COALESCE(t.total_items_purchased, 0) AS INT) AS total_items_purchased,
            CAST(COALESCE(t.items_per_trans, 0.0) AS FLOAT) AS items_per_trans,
            CAST(COALESCE(t.days_since_last_purchase, 999) AS INT) AS days_since_last_purchase,
            CAST(COALESCE(t.trans_count, 0) * 1.0 / (DATE_DIFF('day', c.signup_date, CAST('{cutoff_date}' AS DATE)) / 30.0 + 1.0) AS FLOAT) AS purchase_frequency_per_month,
            CAST(COALESCE(t.trans_count, 0) * 1.0 / (COALESCE(s.total_cart_additions, 0) + 1.0) AS FLOAT) AS cart_conversion_rate,
            CAST(COALESCE(t.days_since_last_purchase, 999) * 1.0 / (COALESCE(s.days_since_last_session, 999) + 1.0) AS FLOAT) AS recency_ratio,
            
            -- Shipping friction & promotions
            CAST(COALESCE(t.trans_discount_usage_rate, 0.0) AS FLOAT) AS trans_discount_usage_rate,
            CAST(COALESCE(t.pct_overnight_shipping, 0.0) AS FLOAT) AS pct_overnight_shipping,
            CAST(COALESCE(t.pct_express_shipping, 0.0) AS FLOAT) AS pct_express_shipping,
            CAST(COALESCE(t.pct_standard_shipping, 0.0) AS FLOAT) AS pct_standard_shipping,
            CAST((COALESCE(s.cart_abandonment_severity, 0) * 1.0 / (COALESCE(s.total_sessions, 0) + 1.0)) * COALESCE(t.pct_overnight_shipping, 0.0) AS FLOAT) AS shipping_friction_score,
            CAST(COALESCE(s.bounce_rate, 0.0) * (COALESCE(s.cart_abandonment_severity, 0) * 1.0 / (COALESCE(s.total_sessions, 0) + 1.0)) AS FLOAT) AS bounce_cart_friction,
            CAST(COALESCE(t.high_value_trans_ratio, 0.0) AS FLOAT) AS high_value_trans_ratio,
            
            -- Channel & device context
            CAST(COALESCE(s.pct_mobile_sessions, 0.0) AS FLOAT) AS pct_mobile_sessions,
            CAST(COALESCE(s.pct_desktop_sessions, 0.0) AS FLOAT) AS pct_desktop_sessions,
            CAST(COALESCE(s.pct_tablet_sessions, 0.0) AS FLOAT) AS pct_tablet_sessions,
            CAST(COALESCE(s.pct_campaign_sessions, 0.0) AS FLOAT) AS pct_campaign_sessions,
            CAST(COALESCE(s.traffic_source_direct_ratio, 0.0) AS FLOAT) AS traffic_source_direct_ratio,
            CAST(COALESCE(s.traffic_source_organic_ratio, 0.0) AS FLOAT) AS traffic_source_organic_ratio,
            CAST(COALESCE(s.traffic_source_paid_ratio, 0.0) AS FLOAT) AS traffic_source_paid_ratio,
            
            -- Geo demographics
            CAST(COALESCE(g.average_income, 50000.0) AS FLOAT) AS average_income,
            CAST(COALESCE(g.urban_ratio, 0.5) AS FLOAT) AS urban_ratio,
            CAST(COALESCE(g.internet_penetration, 0.7) AS FLOAT) AS internet_penetration,
            CAST(COALESCE(t.total_spend, 0.0) / (COALESCE(g.average_income, 50000.0) + 1.0) AS FLOAT) AS spend_to_income_ratio,
            CAST(COALESCE(t.total_spend, 0.0) / (c.credit_limit + 1.0) AS FLOAT) AS credit_utilization_proxy,
            
            -- Noise reduction features
            CAST(c.noise_customer_0 AS FLOAT) AS noise_customer_0,
            CAST(c.noise_customer_1 AS FLOAT) AS noise_customer_1,
            CAST(c.noise_customer_2 AS FLOAT) AS noise_customer_2,
            CAST(c.noise_customer_3 AS FLOAT) AS noise_customer_3,
            CAST(c.noise_customer_4 AS FLOAT) AS noise_customer_4,
            
            -- Target Label: 1 or 0 for train customers, NULL for test customers
            CAST(tr.target AS TINYINT) AS target
        FROM '{healed_dir}/healed_customers.parquet' c
        LEFT JOIN agg_sessions s ON c.customer_id = s.customer_id
        LEFT JOIN agg_transactions t ON c.customer_id = t.customer_id
        LEFT JOIN read_csv_auto('{geo_path}') g ON s.primary_geo_region = g.geo_ip_region
        LEFT JOIN read_csv_auto('{train_path}') tr ON c.customer_id = tr.customer_id
        ORDER BY c.customer_id
    """
    con.execute(feature_store_query)

    total_rows = con.execute("SELECT COUNT(*) FROM customer_features_pit").fetchone()[0]
    labeled_rows = con.execute("SELECT COUNT(*) FROM customer_features_pit WHERE target IS NOT NULL").fetchone()[0]
    unlabeled_rows = con.execute("SELECT COUNT(*) FROM customer_features_pit WHERE target IS NULL").fetchone()[0]
    target_pos = con.execute("SELECT COUNT(*) FROM customer_features_pit WHERE target = 1").fetchone()[0]
    print(f"Total rows in PIT feature store: {total_rows}")
    print(f"Labeled rows (train): {labeled_rows} (Positives: {target_pos}, Rate: {target_pos/labeled_rows:.4f})")
    print(f"Unlabeled rows (test): {unlabeled_rows}")

    # Export to Parquet
    print(f"Saving to {output_parquet}...")
    con.execute(f"COPY customer_features_pit TO '{output_parquet}' (FORMAT PARQUET, COMPRESSION SNAPPY);")

    # Export sample CSV (5,000 rows)
    print(f"Saving sample to {sample_csv}...")
    con.execute(f"COPY (SELECT * FROM customer_features_pit LIMIT 5000) TO '{sample_csv}' (HEADER, DELIMITER ',');")

    # Create Feature Dictionary (tbl_ch3_feature_dictionary.csv)
    print("Generating Feature Dictionary...")
    feature_desc_query = """
        DESCRIBE customer_features_pit
    """
    cols_desc = con.execute(feature_desc_query).df()
    
    # Define business metadata for each feature
    dict_records = []
    category_map = {
        "age": ("Demographics", "Customer age in years", "Direct profile"),
        "account_age_days": ("Demographics", "Days since customer registration to cutoff t0", "t0 - signup_date"),
        "customer_tier_code": ("Demographics", "Ordinal customer tier (1=Bronze, 2=Silver, 3=Gold, 4=Platinum)", "Ordinal mapping"),
        "loyalty_score": ("Demographics", "Loyalty program score (0 to 1)", "Direct profile"),
        "credit_limit": ("Financial", "Assigned credit line in USD", "Direct profile cleaned"),
        "email_open_rate": ("Engagement", "Historical marketing email open rate", "Direct profile"),
        "discount_usage_rate_cust": ("Promotion", "Profile recorded discount usage rate", "Direct profile"),
        "review_score": ("Satisfaction", "Average customer review rating (1 to 5)", "Direct profile"),
        "referral_code": ("Demographics", "Binary flag indicating referral acquisition", "1 if code present else 0"),
        "total_sessions": ("Engagement", "Total website visit sessions up to t0", "SUM(sessions <= t0)"),
        "total_duration_sec": ("Engagement", "Total browsing duration in seconds up to t0", "SUM(duration <= t0)"),
        "avg_session_duration": ("Engagement", "Average duration per session in seconds", "total_duration / total_sessions"),
        "total_pages_viewed": ("Engagement", "Total web pages viewed up to t0", "SUM(pages <= t0)"),
        "avg_pages_per_session": ("Engagement", "Average pages viewed per visit", "total_pages / total_sessions"),
        "bounce_rate": ("Engagement", "Ratio of single-page bounce sessions", "SUM(bounce_flag) / total_sessions"),
        "days_since_last_session": ("Recency", "Days elapsed since the most recent visit", "t0 - MAX(session_timestamp)"),
        "activity_trend_slope": ("Velocity", "Ratio of recent 15-day sessions vs prior 15-day sessions", "sessions[t0-15d, t0] / (sessions[t0-30d, t0-15d] + 1)"),
        "session_frequency_per_month": ("Velocity", "Average number of sessions per active month", "total_sessions / (account_age_days/30 + 1)"),
        "total_cart_additions": ("Cart Barrier", "Total items added to shopping cart up to t0", "SUM(cart_additions <= t0)"),
        "cart_to_page_ratio": ("Cart Barrier", "Intensity of purchase intent vs casual browsing", "total_cart_additions / (total_pages_viewed + 1)"),
        "cart_velocity": ("Cart Barrier", "Average cart additions per session", "total_cart_additions / (total_sessions + 1)"),
        "cart_abandonment_severity": ("Cart Barrier", "Number of sessions with cart additions but no transaction", "SUM(cart_additions > 0 AND no_transaction)"),
        "abandonment_ratio": ("Cart Barrier", "Proportion of abandoned cart sessions", "cart_abandonment_severity / (total_sessions + 1)"),
        "hesitation_index": ("Cart Barrier", "Browsing time invested per cart addition", "total_duration_sec / (total_cart_additions + 1)"),
        "cart_hesitation_ratio": ("Cart Barrier", "Relative deliberation index adjusted for session length", "hesitation_index / (avg_session_duration + 1)"),
        "cart_sessions_ratio": ("Cart Barrier", "Proportion of sessions featuring cart activity", "cart_sessions_count / (total_sessions + 1)"),
        "trans_count": ("Monetary", "Total historical purchases completed up to t0", "COUNT(transactions <= t0)"),
        "total_spend": ("Monetary", "Cumulative monetary expenditure up to t0 (USD)", "SUM(order_value <= t0)"),
        "avg_order_value": ("Monetary", "Average order value (AOV) in USD", "total_spend / trans_count"),
        "max_order_value": ("Monetary", "Maximum historical order value in USD", "MAX(order_value <= t0)"),
        "min_order_value": ("Monetary", "Minimum historical order value in USD", "MIN(order_value <= t0)"),
        "total_items_purchased": ("Monetary", "Total product units purchased historically", "SUM(items_count <= t0)"),
        "items_per_trans": ("Monetary", "Average units per completed transaction", "total_items / trans_count"),
        "days_since_last_purchase": ("Recency", "Days elapsed since the most recent purchase", "t0 - MAX(transaction_timestamp)"),
        "purchase_frequency_per_month": ("Velocity", "Average purchases completed per active month", "trans_count / (account_age_days/30 + 1)"),
        "cart_conversion_rate": ("Cart Barrier", "Conversion rate from cart additions to orders", "trans_count / (total_cart_additions + 1)"),
        "recency_ratio": ("Recency", "Ratio of transaction recency to browsing recency", "days_since_last_purchase / (days_since_last_session + 1)"),
        "trans_discount_usage_rate": ("Promotion", "Proportion of past orders utilizing discount codes", "SUM(discount_applied) / trans_count"),
        "pct_overnight_shipping": ("Friction", "Proportion of orders using premium overnight delivery", "SUM(overnight_shipping) / trans_count"),
        "pct_express_shipping": ("Friction", "Proportion of orders using express shipping", "SUM(express_shipping) / trans_count"),
        "pct_standard_shipping": ("Friction", "Proportion of orders using standard economy shipping", "SUM(standard_shipping) / trans_count"),
        "shipping_friction_score": ("Friction", "Interaction between abandonment ratio and overnight shipping", "abandonment_ratio * pct_overnight_shipping"),
        "bounce_cart_friction": ("Friction", "Interaction between bounce rate and cart abandonment", "bounce_rate * abandonment_ratio"),
        "high_value_trans_ratio": ("Monetary", "Proportion of orders categorized as high-value", "SUM(high_value_flag) / trans_count"),
        "pct_mobile_sessions": ("Context", "Proportion of browsing sessions via mobile device", "mobile_sessions / total_sessions"),
        "pct_desktop_sessions": ("Context", "Proportion of browsing sessions via desktop", "desktop_sessions / total_sessions"),
        "pct_tablet_sessions": ("Context", "Proportion of browsing sessions via tablet device", "tablet_sessions / total_sessions"),
        "pct_campaign_sessions": ("Context", "Proportion of sessions initiated by marketing campaigns", "campaign_sessions / total_sessions"),
        "traffic_source_direct_ratio": ("Context", "Proportion of sessions arriving directly", "direct_sessions / total_sessions"),
        "traffic_source_organic_ratio": ("Context", "Proportion of sessions arriving organically", "organic_sessions / total_sessions"),
        "traffic_source_paid_ratio": ("Context", "Proportion of sessions arriving from paid channels", "paid_sessions / total_sessions"),
        "average_income": ("Macro-Economic", "Regional average resident income from IP geolocation", "geo_data.average_income"),
        "urban_ratio": ("Macro-Economic", "Regional urbanization density ratio [0, 1]", "geo_data.urban_ratio"),
        "internet_penetration": ("Macro-Economic", "Regional broadband internet penetration rate", "geo_data.internet_penetration"),
        "spend_to_income_ratio": ("Macro-Economic", "Ratio of customer spend to regional average income", "total_spend / (average_income + 1)"),
        "credit_utilization_proxy": ("Financial", "Proxy ratio of total spend against credit limit", "total_spend / (credit_limit + 1)"),
        "noise_customer_0": ("Synthetic Noise", "Gaussian noise variable 0 for model robustness testing", "Synthetic random feature"),
        "noise_customer_1": ("Synthetic Noise", "Gaussian noise variable 1 for model robustness testing", "Synthetic random feature"),
        "noise_customer_2": ("Synthetic Noise", "Gaussian noise variable 2 for model robustness testing", "Synthetic random feature"),
        "noise_customer_3": ("Synthetic Noise", "Gaussian noise variable 3 for model robustness testing", "Synthetic random feature"),
        "noise_customer_4": ("Synthetic Noise", "Gaussian noise variable 4 for model robustness testing", "Synthetic random feature"),
        "customer_id": ("Identifier", "Unique customer identification number", "Primary Key"),
        "target": ("Target Label", "Binary purchase indicator in 30-day post-cutoff window", "1 if purchase in (t0, t0+30d], 0 otherwise")
    }

    for _, row in cols_desc.iterrows():
        col_name = row["column_name"]
        dtype = row["column_type"]
        meta = category_map.get(col_name, ("General", "Derived customer feature", "Calculation"))
        dict_records.append({
            "feature_name": col_name,
            "data_type": dtype,
            "category": meta[0],
            "formula": meta[2],
            "business_meaning": meta[1]
        })

    dict_df = pd.DataFrame(dict_records)
    dict_df.to_csv(dictionary_csv, index=False)
    print(f"Feature dictionary with {len(dict_df)} features saved to {dictionary_csv}.")

    con.close()
    gc.collect()


if __name__ == "__main__":
    build_features_pit()
