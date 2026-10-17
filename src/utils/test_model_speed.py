import time
import duckdb
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split

con = duckdb.connect()
df = con.execute("""
    SELECT * EXCLUDE (customer_id)
    FROM 'data/processed/customer_features_pit.parquet'
    WHERE target IS NOT NULL
""").df()
con.close()

X = df.drop(columns=["target"]).values
y = df["target"].values

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print(f"X_train shape: {X_train.shape}, X_val shape: {X_val.shape}")

t0 = time.time()
lgb = LGBMClassifier(n_estimators=100, n_jobs=6, random_state=42, verbose=-1)
lgb.fit(X_train, y_train)
print(f"LGBM fit time: {time.time() - t0:.2f}s")

t0 = time.time()
xgb = XGBClassifier(n_estimators=100, n_jobs=6, random_state=42, tree_method="hist", eval_metric="logloss")
xgb.fit(X_train, y_train)
print(f"XGB fit time: {time.time() - t0:.2f}s")

t0 = time.time()
cb = CatBoostClassifier(iterations=100, thread_count=6, random_seed=42, verbose=0)
cb.fit(X_train, y_train)
print(f"CatBoost fit time: {time.time() - t0:.2f}s")
