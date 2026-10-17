import duckdb
import yaml

with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

con = duckdb.connect()
con.execute(f"SET threads = {config['hardware']['threads']};")
con.execute(f"SET max_memory = '{config['hardware']['duckdb_max_memory']}';")

raw_files = config["raw_files"]
for key, fname in raw_files.items():
    fpath = f"{config['paths']['raw_data_dir']}/{fname}"
    print(f"================ {key} ({fname}) ================")
    try:
        desc = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{fpath}')").df()
        print(desc[['column_name', 'column_type']])
        count = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{fpath}')").fetchone()[0]
        print(f"Total rows: {count}")
        sample = con.execute(f"SELECT * FROM read_csv_auto('{fpath}') LIMIT 3").df()
        print(sample)
    except Exception as e:
        print(f"Error reading {fpath}: {e}")
