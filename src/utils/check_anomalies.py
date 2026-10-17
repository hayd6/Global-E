import duckdb

con = duckdb.connect()

print("--- Checking Date Ranges ---")
print("Customers signup_date range:")
print(con.execute("SELECT MIN(signup_date), MAX(signup_date) FROM read_csv_auto('data/raw/customers.csv')").fetchall())

print("Sessions session_timestamp range:")
print(con.execute("SELECT MIN(session_timestamp), MAX(session_timestamp) FROM read_csv_auto('data/raw/sessions.csv')").fetchall())

print("Transactions transaction_timestamp range:")
print(con.execute("SELECT MIN(transaction_timestamp), MAX(transaction_timestamp) FROM read_csv_auto('data/raw/transactions.csv')").fetchall())

print("\n--- Checking Customers age and credit_limit sample values ---")
print(con.execute("SELECT age, COUNT(*) FROM read_csv_auto('data/raw/customers.csv') WHERE try_cast(age as INT) IS NULL or try_cast(age as INT) < 18 or try_cast(age as INT) > 100 GROUP BY 1 LIMIT 10").df())

print("Credit limit non-numeric or formats:")
print(con.execute("SELECT credit_limit, COUNT(*) FROM read_csv_auto('data/raw/customers.csv') WHERE try_cast(credit_limit as DOUBLE) IS NULL GROUP BY 1 LIMIT 10").df())

print("Customer tiers:")
print(con.execute("SELECT customer_tier, COUNT(*) FROM read_csv_auto('data/raw/customers.csv') GROUP BY 1").df())

print("\n--- Checking Sessions bounce_flag & pages_viewed ---")
print(con.execute("SELECT bounce_flag, COUNT(*) FROM read_csv_auto('data/raw/sessions.csv') GROUP BY 1").df())
print(con.execute("SELECT pages_viewed, COUNT(*) FROM read_csv_auto('data/raw/sessions.csv') WHERE try_cast(pages_viewed as INT) IS NULL GROUP BY 1 LIMIT 10").df())

print("\n--- Checking Transactions order_value, discount_applied, items_count ---")
print(con.execute("SELECT discount_applied, COUNT(*) FROM read_csv_auto('data/raw/transactions.csv') GROUP BY 1").df())
print(con.execute("SELECT shipping_speed, COUNT(*) FROM read_csv_auto('data/raw/transactions.csv') GROUP BY 1").df())
print(con.execute("SELECT items_count <= 0 as bad_items, COUNT(*) FROM read_csv_auto('data/raw/transactions.csv') GROUP BY 1").df())

print("\n--- Checking Temporal Violations ---")
print("Sessions before signup_date:")
print(con.execute("""
    SELECT COUNT(*) 
    FROM read_csv_auto('data/raw/sessions.csv') s
    JOIN read_csv_auto('data/raw/customers.csv') c ON s.customer_id = c.customer_id
    WHERE s.session_timestamp < c.signup_date
""").fetchall())

print("Transactions before signup_date:")
print(con.execute("""
    SELECT COUNT(*) 
    FROM read_csv_auto('data/raw/transactions.csv') t
    JOIN read_csv_auto('data/raw/customers.csv') c ON t.customer_id = c.customer_id
    WHERE t.transaction_timestamp < c.signup_date
""").fetchall())

print("Train target vs future transactions in 2024-06-01 to 2024-07-01:")
print(con.execute("""
    WITH future_tx AS (
        SELECT customer_id, COUNT(*) as tx_count
        FROM read_csv_auto('data/raw/transactions.csv')
        WHERE transaction_timestamp > '2024-06-01' AND transaction_timestamp <= '2024-07-01'
        GROUP BY customer_id
    )
    SELECT tr.target, 
           CASE WHEN f.tx_count IS NOT NULL THEN 1 ELSE 0 END as has_future_tx,
           COUNT(*) as cnt
    FROM read_csv_auto('data/raw/train.csv') tr
    LEFT JOIN future_tx f ON tr.customer_id = f.customer_id
    GROUP BY 1, 2
""").df())
