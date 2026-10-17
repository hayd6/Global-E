import duckdb

con = duckdb.connect()
print('Customers in customers.csv:', con.execute('SELECT COUNT(DISTINCT customer_id) FROM read_csv_auto("data/raw/customers.csv")').fetchone()[0])
print('Customers in train.csv:', con.execute('SELECT COUNT(DISTINCT customer_id) FROM read_csv_auto("data/raw/train.csv")').fetchone()[0])
print('Customers in test.csv:', con.execute('SELECT COUNT(DISTINCT customer_id) FROM read_csv_auto("data/raw/test.csv")').fetchone()[0])
print('Overlap between train and test:', con.execute('SELECT COUNT(*) FROM read_csv_auto("data/raw/train.csv") tr JOIN read_csv_auto("data/raw/test.csv") te ON tr.customer_id = te.customer_id').fetchone()[0])

print('Train target distribution:')
print(con.execute('SELECT target, COUNT(*), COUNT(*)*1.0/160000 FROM read_csv_auto("data/raw/train.csv") GROUP BY 1').df())

# Check if target in train.csv is what the models should train on!
# In DATA DICTIONARY line 90:
# train.csv: customer_id, target (INT8): binary target (1: customer made purchase; 0: did not)
# test.csv: customer_id (40,000 rows)
# In PRD line 37: train.csv (160,000 rows), test.csv (40,000 rows)
# In 03_PROPENSITY_AND_CALIBRATION.md line 25: "Tách tập dữ liệu có nhãn (train.csv ban đầu gồm 160.000 dòng) thành: Train Pool: 80% (128.000 dòng), Holdout Test: 20% (32.000 dòng)"
# In 05_DASHBOARD_WEB_AND_REPORT.md line 26: "target_actual: Nhãn thực tế (1: Mua hàng, 0: Không mua, NULL đối với 40.000 khách hàng tập Test)"
