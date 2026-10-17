import duckdb

con = duckdb.connect()

# Check transactions filtering
q_tx = """
WITH raw_tx AS (
    SELECT t.*, c.signup_date
    FROM read_csv_auto('data/raw/transactions.csv') t
    JOIN read_csv_auto('data/raw/customers.csv') c ON t.customer_id = c.customer_id
)
SELECT 
    COUNT(*) as raw_cnt,
    COUNT(CASE WHEN transaction_timestamp < signup_date THEN 1 END) as time_violation,
    COUNT(CASE WHEN items_count <= 0 AND try_cast(replace(replace(order_value, '$', ''), ',', '') as DOUBLE) > 0 THEN 1 END) as bad_items,
    COUNT(CASE WHEN transaction_timestamp < signup_date OR (items_count <= 0 AND try_cast(replace(replace(order_value, '$', ''), ',', '') as DOUBLE) > 0) THEN 1 END) as total_removed,
    COUNT(CASE WHEN transaction_timestamp >= signup_date AND NOT (items_count <= 0 AND try_cast(replace(replace(order_value, '$', ''), ',', '') as DOUBLE) > 0) THEN 1 END) as healed_cnt
FROM raw_tx
"""
print("Transactions healing audit:")
print(con.execute(q_tx).df())

# Check sessions filtering
q_ses = """
WITH raw_ses AS (
    SELECT s.*, c.signup_date
    FROM read_csv_auto('data/raw/sessions.csv') s
    JOIN read_csv_auto('data/raw/customers.csv') c ON s.customer_id = c.customer_id
)
SELECT 
    COUNT(*) as raw_cnt,
    COUNT(CASE WHEN session_timestamp < signup_date THEN 1 END) as time_violation,
    COUNT(CASE WHEN session_timestamp >= signup_date THEN 1 END) as healed_cnt
FROM raw_ses
"""
print("Sessions healing audit:")
print(con.execute(q_ses).df())
