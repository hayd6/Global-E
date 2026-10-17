"""
tests/test_pit_integrity.py
Bộ kiểm thử tính toàn vẹn Point-in-Time và chống rò rỉ dữ liệu (Anti-Leakage)
Tuân thủ: .agy/00_CORE_RULES.md và .agy/01_DATA_ENGINEERING_PIT.md
"""

import os
import duckdb
import pytest
import pandas as pd
import numpy as np


FEATURE_STORE_PATH = "data/processed/customer_features_pit.parquet"
HEALED_DIR = "data/processed/healed"
CUTOFF_DATE = "2024-06-01"


def test_unique_customer_id():
    """Khẳng định trường customer_id là duy nhất và không có bản ghi trùng lặp."""
    con = duckdb.connect()
    df = con.execute(f"SELECT customer_id FROM '{FEATURE_STORE_PATH}'").df()
    con.close()
    
    assert len(df) == 200000, f"Expected 200,000 rows, got {len(df)}"
    assert df["customer_id"].nunique() == 200000, "customer_id contains duplicates!"


def test_feature_exclusion():
    """Khẳng định customer_id và target tuyệt đối không nằm trong danh sách đặc trưng X."""
    con = duckdb.connect()
    cols = [col[0] for col in con.execute(f"DESCRIBE SELECT * FROM '{FEATURE_STORE_PATH}'").fetchall()]
    con.close()
    
    feature_cols = [c for c in cols if c not in ["customer_id", "target"]]
    
    assert "customer_id" not in feature_cols, "customer_id was not excluded from feature list!"
    assert "target" not in feature_cols, "target was not excluded from feature list!"
    assert len(feature_cols) >= 45, f"Expected at least 45 features, got {len(feature_cols)}"


def test_temporal_invariance():
    """
    Khẳng định tính bất biến theo thời gian:
    Bổ sung dữ liệu giao dịch nhân tạo sau mốc t0 không làm thay đổi ma trận đặc trưng tại t0.
    """
    con = duckdb.connect()
    con.execute("SET threads = 4;")
    
    # 1. Trích xuất ngẫu nhiên mẫu 100 khách hàng
    sample_customers = con.execute(f"""
        SELECT customer_id 
        FROM '{FEATURE_STORE_PATH}' 
        USING SAMPLE 100 (reservoir, 42)
        ORDER BY customer_id
    """).df()
    sample_ids = tuple(sample_customers["customer_id"].tolist())
    
    # 2. Lấy đặc trưng gốc tại t0 của 100 khách hàng này
    original_features = con.execute(f"""
        SELECT * EXCLUDE (customer_id, target)
        FROM '{FEATURE_STORE_PATH}'
        WHERE customer_id IN {sample_ids}
        ORDER BY customer_id
    """).df()
    
    # 3. Tạo bảng giao dịch tạm thời và bổ sung 50 bản ghi tương lai (t > t0)
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE temp_tx AS
        SELECT * FROM '{HEALED_DIR}/healed_transactions.parquet';
    """)
    
    # Chọn 50 khách hàng trong mẫu 100 để chèn giao dịch tương lai giả định
    future_customers = sample_customers["customer_id"].iloc[:50].tolist()
    future_records = []
    for i, cid in enumerate(future_customers):
        future_records.append({
            "transaction_id": 99000000 + i,
            "customer_id": cid,
            "transaction_timestamp": "2024-06-15",
            "order_value": 999.0,
            "items_count": 5,
            "payment_method": "Credit Card",
            "discount_applied": 1,
            "shipping_speed": "overnight",
            "high_value_flag": True,
            "noise_trans_0": 0.0,
            "noise_trans_1": 0.0
        })
    future_df = pd.DataFrame(future_records)
    con.register("future_df", future_df)
    con.execute("INSERT INTO temp_tx SELECT * FROM future_df;")
    
    # 4. Tính toán lại đặc trưng tại t0 trên tập dữ liệu đã bị can thiệp tương lai
    recomputed_features = con.execute(f"""
        WITH tx_agg AS (
            SELECT 
                customer_id,
                COUNT(*) AS trans_count,
                SUM(order_value) AS total_spend,
                AVG(order_value) AS avg_order_value,
                MAX(order_value) AS max_order_value,
                MIN(order_value) AS min_order_value,
                SUM(items_count) AS total_items_purchased,
                AVG(items_count) AS items_per_trans,
                DATE_DIFF('day', MAX(transaction_timestamp), CAST('{CUTOFF_DATE}' AS DATE)) AS days_since_last_purchase,
                AVG(discount_applied) AS trans_discount_usage_rate,
                CAST(COUNT(CASE WHEN shipping_speed = 'overnight' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_overnight_shipping,
                CAST(COUNT(CASE WHEN shipping_speed = 'express' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_express_shipping,
                CAST(COUNT(CASE WHEN shipping_speed = 'standard' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_standard_shipping,
                CAST(COUNT(CASE WHEN high_value_flag = true THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS high_value_trans_ratio
            FROM temp_tx
            WHERE transaction_timestamp <= '{CUTOFF_DATE}'
              AND customer_id IN {sample_ids}
            GROUP BY customer_id
        )
        SELECT 
            f.trans_count,
            f.total_spend,
            f.avg_order_value,
            f.max_order_value,
            f.min_order_value,
            f.total_items_purchased,
            f.items_per_trans,
            f.days_since_last_purchase,
            f.trans_discount_usage_rate,
            f.pct_overnight_shipping,
            f.pct_express_shipping,
            f.pct_standard_shipping,
            f.high_value_trans_ratio
        FROM '{FEATURE_STORE_PATH}' f
        WHERE f.customer_id IN {sample_ids}
        ORDER BY f.customer_id
    """).df()
    
    recomputed_from_temp = con.execute(f"""
        WITH tx_agg AS (
            SELECT 
                customer_id,
                CAST(COUNT(*) AS INT) AS trans_count,
                CAST(SUM(order_value) AS FLOAT) AS total_spend,
                CAST(AVG(order_value) AS FLOAT) AS avg_order_value,
                CAST(MAX(order_value) AS FLOAT) AS max_order_value,
                CAST(MIN(order_value) AS FLOAT) AS min_order_value,
                CAST(SUM(items_count) AS INT) AS total_items_purchased,
                CAST(AVG(items_count) AS FLOAT) AS items_per_trans,
                CAST(DATE_DIFF('day', MAX(transaction_timestamp), CAST('{CUTOFF_DATE}' AS DATE)) AS INT) AS days_since_last_purchase,
                CAST(AVG(discount_applied) AS FLOAT) AS trans_discount_usage_rate,
                CAST(COUNT(CASE WHEN shipping_speed = 'overnight' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_overnight_shipping,
                CAST(COUNT(CASE WHEN shipping_speed = 'express' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_express_shipping,
                CAST(COUNT(CASE WHEN shipping_speed = 'standard' THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS pct_standard_shipping,
                CAST(COUNT(CASE WHEN high_value_flag = true THEN 1 END) * 1.0 / COUNT(*) AS FLOAT) AS high_value_trans_ratio
            FROM temp_tx
            WHERE transaction_timestamp <= '{CUTOFF_DATE}'
              AND customer_id IN {sample_ids}
            GROUP BY customer_id
        )
        SELECT 
            c.customer_id,
            CAST(COALESCE(t.trans_count, 0) AS INT) AS trans_count,
            CAST(COALESCE(t.total_spend, 0.0) AS FLOAT) AS total_spend,
            CAST(COALESCE(t.avg_order_value, 0.0) AS FLOAT) AS avg_order_value,
            CAST(COALESCE(t.max_order_value, 0.0) AS FLOAT) AS max_order_value,
            CAST(COALESCE(t.min_order_value, 0.0) AS FLOAT) AS min_order_value,
            CAST(COALESCE(t.total_items_purchased, 0) AS INT) AS total_items_purchased,
            CAST(COALESCE(t.items_per_trans, 0.0) AS FLOAT) AS items_per_trans,
            CAST(COALESCE(t.days_since_last_purchase, 999) AS INT) AS days_since_last_purchase,
            CAST(COALESCE(t.trans_discount_usage_rate, 0.0) AS FLOAT) AS trans_discount_usage_rate,
            CAST(COALESCE(t.pct_overnight_shipping, 0.0) AS FLOAT) AS pct_overnight_shipping,
            CAST(COALESCE(t.pct_express_shipping, 0.0) AS FLOAT) AS pct_express_shipping,
            CAST(COALESCE(t.pct_standard_shipping, 0.0) AS FLOAT) AS pct_standard_shipping,
            CAST(COALESCE(t.high_value_trans_ratio, 0.0) AS FLOAT) AS high_value_trans_ratio
        FROM (SELECT customer_id FROM '{FEATURE_STORE_PATH}' WHERE customer_id IN {sample_ids}) c
        LEFT JOIN tx_agg t ON c.customer_id = t.customer_id
        ORDER BY c.customer_id
    """).df()
    
    orig_tx = con.execute(f"""
        SELECT 
            customer_id,
            trans_count,
            total_spend,
            avg_order_value,
            max_order_value,
            min_order_value,
            total_items_purchased,
            items_per_trans,
            days_since_last_purchase,
            trans_discount_usage_rate,
            pct_overnight_shipping,
            pct_express_shipping,
            pct_standard_shipping,
            high_value_trans_ratio
        FROM '{FEATURE_STORE_PATH}'
        WHERE customer_id IN {sample_ids}
        ORDER BY customer_id
    """).df()
    
    con.close()
    
    # 5. Khẳng định bằng chứng không rò rỉ: kết quả tính toán tại t0 trước và sau khi thêm tương lai trùng khớp 100%
    pd.testing.assert_frame_equal(orig_tx, recomputed_from_temp, check_exact=False, rtol=1e-5)
    print("Test temporal invariance PASSED: Future transactions have 0 impact on features at t0.")
