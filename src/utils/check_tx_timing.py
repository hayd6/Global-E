import duckdb

con = duckdb.connect()

print("--- Check transactions in different date ranges ---")
print(con.execute("""
    SELECT 
        COUNT(*) as total_trans,
        COUNT(CASE WHEN transaction_timestamp > '2024-06-01' THEN 1 END) as after_cutoff,
        COUNT(CASE WHEN transaction_timestamp > '2024-06-01' AND transaction_timestamp <= '2024-07-01' THEN 1 END) as window_30d,
        COUNT(CASE WHEN transaction_timestamp <= '2024-06-01' THEN 1 END) as before_cutoff
    FROM read_csv_auto('data/raw/transactions.csv')
""").df())

print("--- Check how train.csv target was created or what target represents ---")
# Let's see if target in train.csv matches transactions or if train.csv IS the ground truth target
# Check customer_features_pit requirement:
# "Lưu trữ toàn bộ bảng đặc trưng của 200.000 khách hàng ra file: data/processed/customer_features_pit.parquet"
# "Tách tập dữ liệu có nhãn (train.csv ban đầu gồm 160.000 dòng) thành: Train Pool: 80% (128.000 dòng), Holdout Test: 20% (32.000 dòng)"
