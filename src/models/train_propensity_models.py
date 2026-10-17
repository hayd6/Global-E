"""
src/models/train_propensity_models.py
Huấn luyện mô hình phân loại chuyển đổi, tối ưu hóa siêu tham số bằng Optuna,
và xây dựng mô hình tổ hợp xếp chồng (Stacking Ensemble).
Tuân thủ: .agy/00_CORE_RULES.md và .agy/03_PROPENSITY_AND_CALIBRATION.md
"""

import os
import sys
import gc
import time
import pickle
import yaml
import duckdb
import optuna
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

optuna.logging.set_verbosity(optuna.logging.WARNING)


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class EarlyStoppingCallback:
    """Optuna callback dừng sớm sau n_trials_without_improvement không cải thiện."""
    def __init__(self, early_stopping_rounds=7):
        self.early_stopping_rounds = early_stopping_rounds
        self._best_value = -np.inf
        self._no_improvement_count = 0

    def __call__(self, study: optuna.Study, trial: optuna.Trial):
        current_value = trial.value
        if current_value is None:
            return
        if current_value > self._best_value + 1e-4:
            self._best_value = current_value
            self._no_improvement_count = 0
        else:
            self._no_improvement_count += 1
            if self._no_improvement_count >= self.early_stopping_rounds:
                study.stop()


def run_training_pipeline():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]
    experiments_dir = config["paths"]["experiments_dir"]
    feature_store_path = config["paths"]["feature_store_path"]

    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(experiments_dir, exist_ok=True)

    n_jobs = config["hardware"]["threads"]
    random_state = config["data_split"]["random_state"]
    n_trials = config["optuna"]["n_trials"]
    early_stopping_rounds = config["optuna"]["early_stopping_rounds"]

    print("--- 1. Loading Feature Store and Splitting Data ---")
    con = duckdb.connect()
    df = con.execute(f"""
        SELECT * EXCLUDE (customer_id)
        FROM '{feature_store_path}'
        WHERE target IS NOT NULL
        ORDER BY customer_id
    """).df()
    cust_ids = con.execute(f"""
        SELECT customer_id 
        FROM '{feature_store_path}'
        WHERE target IS NOT NULL
        ORDER BY customer_id
    """).df()["customer_id"].values
    con.close()

    feature_cols = [c for c in df.columns if c != "target"]
    X = df[feature_cols].values
    y = df["target"].values.astype(int)

    # Stratified 80/20 Train Pool vs Holdout Test
    skf_outer = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    train_idx, holdout_idx = next(skf_outer.split(X, y))

    X_train, y_train = X[train_idx], y[train_idx]
    X_holdout, y_holdout = X[holdout_idx], y[holdout_idx]
    train_cust_ids = cust_ids[train_idx]
    holdout_cust_ids = cust_ids[holdout_idx]

    print(f"Train Pool shape: {X_train.shape} (Positives: {np.sum(y_train)}, Rate: {np.mean(y_train):.4f})")
    print(f"Holdout Test shape: {X_holdout.shape} (Positives: {np.sum(y_holdout)}, Rate: {np.mean(y_holdout):.4f})")

    # Save split indices
    split_indices_path = os.path.join(experiments_dir, "split_indices.npz")
    np.savez_compressed(
        split_indices_path,
        train_indices=train_idx,
        holdout_indices=holdout_idx,
        train_customer_ids=train_cust_ids,
        holdout_customer_ids=holdout_cust_ids
    )
    print(f"Split indices saved to {split_indices_path}")

    # Median Imputation on Train, transform on Holdout (Anti-leakage)
    print("Fitting SimpleImputer(strategy='median') on Train Pool...")
    imputer = SimpleImputer(strategy="median")
    X_train_imp = imputer.fit_transform(X_train)
    X_holdout_imp = imputer.transform(X_holdout)

    # Prepare Scaler for linear models
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_imp)
    X_holdout_scaled = scaler.transform(X_holdout_imp)

    trained_models = {}
    training_times = {}

    # --- 2. Train Baselines ---
    print("\n--- 2. Training Baseline Models ---")
    # Logistic Regression
    t0 = time.time()
    lr = LogisticRegression(max_iter=1000, random_state=random_state)
    lr.fit(X_train_scaled, y_train)
    training_times["Logistic Regression"] = time.time() - t0
    trained_models["Logistic Regression"] = lr
    print(f"Logistic Regression trained in {training_times['Logistic Regression']:.2f}s")

    # Random Forest
    t0 = time.time()
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=20,
        n_jobs=n_jobs,
        random_state=random_state
    )
    rf.fit(X_train_imp, y_train)
    training_times["Random Forest"] = time.time() - t0
    trained_models["Random Forest"] = rf
    print(f"Random Forest trained in {training_times['Random Forest']:.2f}s")

    # --- 3. Hyperparameter Optimization with Optuna ---
    print("\n--- 3. Hyperparameter Optimization with Optuna (35 Trials / Early Stopping 7) ---")
    # For HPO speed and stability, use 3-fold stratified validation with subsample
    hpo_skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=random_state)
    np.random.seed(random_state)
    hpo_sub_idx = np.random.choice(len(X_train_imp), size=40000, replace=False)
    X_hpo, y_hpo = X_train_imp[hpo_sub_idx], y_train[hpo_sub_idx]

    best_hyperparams_records = []

    # 3.1 LightGBM
    print("\n[Optuna] Optimizing LightGBM...")
    def objective_lgb(trial):
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 15, 127),
            "max_depth": trial.suggest_int("max_depth", 4, 10),
            "min_child_samples": trial.suggest_int("min_child_samples", 20, 200),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1.0, 5.0),
            "n_estimators": 80,
            "n_jobs": n_jobs,
            "random_state": random_state,
            "verbose": -1
        }
        scores = []
        for tr_i, val_i in hpo_skf.split(X_hpo, y_hpo):
            clf = LGBMClassifier(**params)
            clf.fit(X_hpo[tr_i], y_hpo[tr_i])
            preds = clf.predict_proba(X_hpo[val_i])[:, 1]
            scores.append(average_precision_score(y_hpo[val_i], preds))
        return float(np.mean(scores))

    study_lgb = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=random_state))
    study_lgb.optimize(objective_lgb, n_trials=n_trials, callbacks=[EarlyStoppingCallback(early_stopping_rounds)])
    print(f"LightGBM Best Trial: PR-AUC = {study_lgb.best_value:.4f}")
    best_lgb_params = study_lgb.best_params.copy()
    best_lgb_params.update({"n_estimators": 150, "n_jobs": n_jobs, "random_state": random_state, "verbose": -1})
    
    t0 = time.time()
    best_lgb = LGBMClassifier(**best_lgb_params)
    best_lgb.fit(X_train_imp, y_train)
    training_times["LightGBM"] = time.time() - t0
    trained_models["LightGBM"] = best_lgb

    for k, v in study_lgb.best_params.items():
        best_hyperparams_records.append({
            "model_family": "LightGBM",
            "hyperparameter": k,
            "optimal_value": round(float(v), 4) if isinstance(v, float) else v,
            "best_cv_pr_auc": round(study_lgb.best_value, 4)
        })

    # 3.2 CatBoost
    print("\n[Optuna] Optimizing CatBoost...")
    def objective_cb(trial):
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
            "depth": trial.suggest_int("depth", 4, 7),
            "l2_leaf_reg": trial.suggest_int("l2_leaf_reg", 1, 10),
            "random_strength": trial.suggest_float("random_strength", 0.1, 10.0),
            "iterations": 80,
            "thread_count": n_jobs,
            "random_seed": random_state,
            "auto_class_weights": "Balanced",
            "verbose": 0
        }
        scores = []
        for tr_i, val_i in hpo_skf.split(X_hpo, y_hpo):
            clf = CatBoostClassifier(**params)
            clf.fit(X_hpo[tr_i], y_hpo[tr_i])
            preds = clf.predict_proba(X_hpo[val_i])[:, 1]
            scores.append(average_precision_score(y_hpo[val_i], preds))
        return float(np.mean(scores))

    study_cb = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=random_state))
    study_cb.optimize(objective_cb, n_trials=n_trials, callbacks=[EarlyStoppingCallback(early_stopping_rounds)])
    print(f"CatBoost Best Trial: PR-AUC = {study_cb.best_value:.4f}")
    best_cb_params = study_cb.best_params.copy()
    best_cb_params.update({"iterations": 150, "thread_count": n_jobs, "random_seed": random_state, "auto_class_weights": "Balanced", "verbose": 0})
    
    t0 = time.time()
    best_cb = CatBoostClassifier(**best_cb_params)
    best_cb.fit(X_train_imp, y_train)
    training_times["CatBoost"] = time.time() - t0
    trained_models["CatBoost"] = best_cb

    for k, v in study_cb.best_params.items():
        best_hyperparams_records.append({
            "model_family": "CatBoost",
            "hyperparameter": k,
            "optimal_value": round(float(v), 4) if isinstance(v, float) else v,
            "best_cv_pr_auc": round(study_cb.best_value, 4)
        })

    # 3.3 XGBoost
    print("\n[Optuna] Optimizing XGBoost...")
    def objective_xgb(trial):
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.15, log=True),
            "max_depth": trial.suggest_int("max_depth", 4, 7),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "scale_pos_weight": trial.suggest_float("scale_pos_weight", 1.0, 5.0),
            "n_estimators": 80,
            "n_jobs": n_jobs,
            "random_state": random_state,
            "tree_method": "hist",
            "eval_metric": "logloss"
        }
        scores = []
        for tr_i, val_i in hpo_skf.split(X_hpo, y_hpo):
            clf = XGBClassifier(**params)
            clf.fit(X_hpo[tr_i], y_hpo[tr_i])
            preds = clf.predict_proba(X_hpo[val_i])[:, 1]
            scores.append(average_precision_score(y_hpo[val_i], preds))
        return float(np.mean(scores))

    study_xgb = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=random_state))
    study_xgb.optimize(objective_xgb, n_trials=n_trials, callbacks=[EarlyStoppingCallback(early_stopping_rounds)])
    print(f"XGBoost Best Trial: PR-AUC = {study_xgb.best_value:.4f}")
    best_xgb_params = study_xgb.best_params.copy()
    best_xgb_params.update({"n_estimators": 150, "n_jobs": n_jobs, "random_state": random_state, "tree_method": "hist", "eval_metric": "logloss"})
    
    t0 = time.time()
    best_xgb = XGBClassifier(**best_xgb_params)
    best_xgb.fit(X_train_imp, y_train)
    training_times["XGBoost"] = time.time() - t0
    trained_models["XGBoost"] = best_xgb

    for k, v in study_xgb.best_params.items():
        best_hyperparams_records.append({
            "model_family": "XGBoost",
            "hyperparameter": k,
            "optimal_value": round(float(v), 4) if isinstance(v, float) else v,
            "best_cv_pr_auc": round(study_xgb.best_value, 4)
        })

    # Save best hyperparameters table
    hparams_df = pd.DataFrame(best_hyperparams_records)
    hparams_csv = os.path.join(tables_dir, "tbl_ch4_optuna_best_hyperparameters.csv")
    hparams_df.to_csv(hparams_csv, index=False)
    print(f"\nBest hyperparameters saved to {hparams_csv}")

    # --- 4. Stacking Ensemble ---
    print("\n--- 4. Building Stacking Ensemble ---")
    cv_stack = StratifiedKFold(n_splits=3, shuffle=True, random_state=random_state)
    oof_preds = np.zeros((len(X_train_imp), 3), dtype=np.float32)
    t0 = time.time()
    for tr_i, val_i in cv_stack.split(X_train_imp, y_train):
        # Fold LGBM
        m_lgb = LGBMClassifier(**best_lgb_params)
        m_lgb.fit(X_train_imp[tr_i], y_train[tr_i])
        oof_preds[val_i, 0] = m_lgb.predict_proba(X_train_imp[val_i])[:, 1]
        
        # Fold CatBoost
        m_cb = CatBoostClassifier(**best_cb_params)
        m_cb.fit(X_train_imp[tr_i], y_train[tr_i])
        oof_preds[val_i, 1] = m_cb.predict_proba(X_train_imp[val_i])[:, 1]
        
        # Fold Random Forest
        m_rf = RandomForestClassifier(n_estimators=100, max_depth=10, n_jobs=n_jobs, random_state=random_state)
        m_rf.fit(X_train_imp[tr_i], y_train[tr_i])
        oof_preds[val_i, 2] = m_rf.predict_proba(X_train_imp[val_i])[:, 1]

    # Meta-learner: Logistic Regression
    meta_learner = LogisticRegression(random_state=random_state)
    meta_learner.fit(oof_preds, y_train)
    training_times["Stacking Ensemble"] = time.time() - t0
    trained_models["Stacking Meta-Learner"] = meta_learner
    print(f"Stacking Ensemble trained in {training_times['Stacking Ensemble']:.2f}s (Meta-weights: {meta_learner.coef_})")

    # Save trained models and preprocessed holdout data for calibration & evaluation
    checkpoint_data = {
        "feature_cols": feature_cols,
        "trained_models": trained_models,
        "training_times": training_times,
        "imputer": imputer,
        "scaler": scaler,
        "X_train_imp": X_train_imp,
        "X_train_scaled": X_train_scaled,
        "y_train": y_train,
        "X_holdout_imp": X_holdout_imp,
        "X_holdout_scaled": X_holdout_scaled,
        "y_holdout": y_holdout,
        "best_lgb_params": best_lgb_params,
        "best_cb_params": best_cb_params,
        "best_xgb_params": best_xgb_params
    }
    ckpt_path = os.path.join(models_dir, "propensity_checkpoint.pkl")
    with open(ckpt_path, "wb") as f:
        pickle.dump(checkpoint_data, f)
    print(f"\nCheckpoint successfully saved to {ckpt_path}")

    gc.collect()


if __name__ == "__main__":
    run_training_pipeline()
