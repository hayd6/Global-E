"""
src/models/calibrate_and_evaluate.py
Hiệu chỉnh xác suất thực nghiệm (Probability Calibration) bằng Isotonic Regression & Platt Scaling,
đo lường Brier Score, ECE và xuất bảng benchmark so sánh toàn diện 10 chỉ số trên Holdout Test (32,000 dòng).
Tuân thủ: .agy/00_CORE_RULES.md và .agy/03_PROPENSITY_AND_CALIBRATION.md
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import gc
import time
import pickle
import yaml
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    brier_score_loss
)
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from src.models.pipeline_wrapper import FullPipelineModel

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def compute_ece(y_true, y_prob, n_bins=10):
    """Tính Expected Calibration Error (ECE) với n_bins phân vị đều."""
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    total_samples = len(y_true)
    for i in range(n_bins):
        bin_mask = (y_prob >= bin_edges[i]) & (y_prob < bin_edges[i + 1])
        if i == n_bins - 1:
            bin_mask = bin_mask | (y_prob == 1.0)
        bin_count = np.sum(bin_mask)
        if bin_count > 0:
            bin_acc = np.mean(y_true[bin_mask])
            bin_conf = np.mean(y_prob[bin_mask])
            ece += (bin_count / total_samples) * np.abs(bin_acc - bin_conf)
    return float(ece)


def run_calibration_and_evaluation():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]

    # Load checkpoint from step 3.1
    ckpt_path = os.path.join(models_dir, "propensity_checkpoint.pkl")
    print(f"Loading checkpoint from {ckpt_path}...")
    with open(ckpt_path, "rb") as f:
        ckpt = pickle.load(f)

    feature_cols = ckpt["feature_cols"]
    trained_models = ckpt["trained_models"]
    training_times = ckpt["training_times"]
    imputer = ckpt["imputer"]
    X_train_imp = ckpt["X_train_imp"]
    y_train = ckpt["y_train"]
    X_holdout_imp = ckpt["X_holdout_imp"]
    X_holdout_scaled = ckpt["X_holdout_scaled"]
    y_holdout = ckpt["y_holdout"]
    best_lgb_params = ckpt["best_lgb_params"]
    best_cb_params = ckpt["best_cb_params"]

    print(f"Evaluating models on Holdout Test (N = {len(y_holdout):,}, Positives: {np.sum(y_holdout):,})...")

    # --- 1. Train Calibration Models on LightGBM ---
    print("\n--- Training Calibrated Models on Best LightGBM ---")
    base_lgbm = LGBMClassifier(**best_lgb_params)

    # 1.1 Isotonic Calibration
    t0 = time.time()
    calib_isotonic = CalibratedClassifierCV(estimator=base_lgbm, method="isotonic", cv=3)
    calib_isotonic.fit(X_train_imp, y_train)
    time_iso = time.time() - t0
    trained_models["Calibrated LightGBM (Isotonic)"] = calib_isotonic
    training_times["Calibrated LightGBM (Isotonic)"] = time_iso
    print(f"Isotonic Calibration fitted in {time_iso:.2f}s")

    # 1.2 Sigmoid / Platt Scaling Calibration
    t0 = time.time()
    calib_sigmoid = CalibratedClassifierCV(estimator=base_lgbm, method="sigmoid", cv=3)
    calib_sigmoid.fit(X_train_imp, y_train)
    time_sig = time.time() - t0
    trained_models["Calibrated LightGBM (Platt Sigmoid)"] = calib_sigmoid
    training_times["Calibrated LightGBM (Platt Sigmoid)"] = time_sig
    print(f"Platt Sigmoid Calibration fitted in {time_sig:.2f}s")

    # Save calibration curves data for plot_model_evaluation.py
    lgbm_prob = trained_models["LightGBM"].predict_proba(X_holdout_imp)[:, 1]
    iso_prob = calib_isotonic.predict_proba(X_holdout_imp)[:, 1]
    sig_prob = calib_sigmoid.predict_proba(X_holdout_imp)[:, 1]

    calib_data = {
        "y_holdout": y_holdout,
        "lgbm_prob": lgbm_prob,
        "iso_prob": iso_prob,
        "sig_prob": sig_prob
    }
    with open(os.path.join(models_dir, "calibration_eval_data.pkl"), "wb") as f:
        pickle.dump(calib_data, f)

    # --- 2. Benchmark All Models on Holdout Test ---
    print("\n--- Benchmarking All Models on Holdout Test ---")
    models_to_eval = [
        ("Logistic Regression", trained_models["Logistic Regression"], X_holdout_scaled),
        ("Random Forest", trained_models["Random Forest"], X_holdout_imp),
        ("XGBoost", trained_models["XGBoost"], X_holdout_imp),
        ("CatBoost", trained_models["CatBoost"], X_holdout_imp),
        ("LightGBM", trained_models["LightGBM"], X_holdout_imp),
        ("Calibrated LightGBM (Isotonic)", calib_isotonic, X_holdout_imp),
        ("Calibrated LightGBM (Platt Sigmoid)", calib_sigmoid, X_holdout_imp)
    ]

    # Stacking ensemble predictions on holdout
    stacking_meta = trained_models["Stacking Meta-Learner"]
    t0 = time.time()
    lgb_p = trained_models["LightGBM"].predict_proba(X_holdout_imp)[:, 1]
    cb_p = trained_models["CatBoost"].predict_proba(X_holdout_imp)[:, 1]
    rf_p = trained_models["Random Forest"].predict_proba(X_holdout_imp)[:, 1]
    holdout_oof = np.column_stack([lgb_p, cb_p, rf_p])
    stack_preds_prob = stacking_meta.predict_proba(holdout_oof)[:, 1]
    stack_latency = (time.time() - t0) * 1000.0 / len(y_holdout)

    benchmark_records = []
    holdout_prob_dict = {}

    for m_name, model, X_eval in models_to_eval:
        # Measure inference latency per sample in ms
        t0 = time.time()
        probs = model.predict_proba(X_eval)[:, 1]
        t_infer = time.time() - t0
        latency_ms = round((t_infer * 1000.0) / len(y_holdout), 4)
        holdout_prob_dict[m_name] = probs

        # Metrics at default threshold 0.5
        preds_binary = (probs >= 0.5).astype(int)

        pr_auc = round(float(average_precision_score(y_holdout, probs)), 4)
        roc_auc = round(float(roc_auc_score(y_holdout, probs)), 4)
        f1 = round(float(f1_score(y_holdout, preds_binary, zero_division=0)), 4)
        prec = round(float(precision_score(y_holdout, preds_binary, zero_division=0)), 4)
        rec = round(float(recall_score(y_holdout, preds_binary, zero_division=0)), 4)
        acc = round(float(accuracy_score(y_holdout, preds_binary)), 4)
        brier = round(float(brier_score_loss(y_holdout, probs)), 4)
        ece = round(compute_ece(y_holdout, probs, n_bins=10), 4)
        fit_t = round(float(training_times.get(m_name, 0.0)), 2)

        benchmark_records.append({
            "model_name": m_name,
            "pr_auc": pr_auc,
            "roc_auc": roc_auc,
            "f1_score": f1,
            "precision": prec,
            "recall": rec,
            "accuracy": acc,
            "brier_score": brier,
            "ece": ece,
            "fit_time_sec": fit_t,
            "inference_latency_ms": latency_ms
        })

    # Add Stacking Ensemble to benchmark
    holdout_prob_dict["Stacking Ensemble"] = stack_preds_prob
    stack_binary = (stack_preds_prob >= 0.5).astype(int)
    benchmark_records.append({
        "model_name": "Stacking Ensemble",
        "pr_auc": round(float(average_precision_score(y_holdout, stack_preds_prob)), 4),
        "roc_auc": round(float(roc_auc_score(y_holdout, stack_preds_prob)), 4),
        "f1_score": round(float(f1_score(y_holdout, stack_binary, zero_division=0)), 4),
        "precision": round(float(precision_score(y_holdout, stack_binary, zero_division=0)), 4),
        "recall": round(float(recall_score(y_holdout, stack_binary, zero_division=0)), 4),
        "accuracy": round(float(accuracy_score(y_holdout, stack_binary)), 4),
        "brier_score": round(float(brier_score_loss(y_holdout, stack_preds_prob)), 4),
        "ece": round(compute_ece(y_holdout, stack_preds_prob, n_bins=10), 4),
        "fit_time_sec": round(float(training_times.get("Stacking Ensemble", 0.0)), 2),
        "inference_latency_ms": round(stack_latency, 4)
    })

    # Export benchmark comparison table
    benchmark_df = pd.DataFrame(benchmark_records).sort_values("pr_auc", ascending=False)
    benchmark_csv = os.path.join(tables_dir, "tbl_ch4_model_benchmark_comparison.csv")
    benchmark_df.to_csv(benchmark_csv, index=False)
    print(f"\nModel Benchmark Comparison saved to {benchmark_csv}:")
    print(benchmark_df.to_string(index=False))

    # --- 3. Save Best Calibrated Model ---
    # Select best model: lowest Brier Score & ECE among top boosting models
    # Calibrated LightGBM (Isotonic) or Platt Sigmoid
    brier_iso = brier_score_loss(y_holdout, iso_prob)
    brier_sig = brier_score_loss(y_holdout, sig_prob)
    selected_calib_model = calib_isotonic if brier_iso <= brier_sig else calib_sigmoid
    selected_name = "Isotonic" if brier_iso <= brier_sig else "Platt Sigmoid"
    print(f"\nSelected Best Calibrated Model: Calibrated LightGBM ({selected_name})")

    # Wrap with Imputer and feature columns
    best_pipeline = FullPipelineModel(
        imputer=imputer,
        model=selected_calib_model,
        feature_cols=feature_cols
    )

    best_model_path = os.path.join(models_dir, "best_calibrated_model.pkl")
    with open(best_model_path, "wb") as f:
        pickle.dump(best_pipeline, f)
    print(f"Exported best calibrated model to {best_model_path}")

    # Save holdout predictions for all models for ROC / PR plotting
    with open(os.path.join(models_dir, "holdout_predictions.pkl"), "wb") as f:
        pickle.dump({"y_holdout": y_holdout, "probs": holdout_prob_dict}, f)

    gc.collect()


if __name__ == "__main__":
    run_calibration_and_evaluation()
