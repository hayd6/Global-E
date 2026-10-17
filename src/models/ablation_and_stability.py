"""
src/models/ablation_and_stability.py
Thực nghiệm chuyên sâu: Ablation Study (Đo lường giá trị thông tin của từng nhóm biến)
và Kiểm định độ ổn định qua 5 hạt giống ngẫu nhiên (Multi-Seed Testing).
Tuân thủ: .agy/00_CORE_RULES.md và .agy/03_PROPENSITY_AND_CALIBRATION.md
"""

import os
import sys
import gc
import time
import pickle
import yaml
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score, f1_score, brier_score_loss
from lightgbm import LGBMClassifier

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_ablation_and_stability():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]

    # Load checkpoint
    ckpt_path = os.path.join(models_dir, "propensity_checkpoint.pkl")
    print(f"Loading checkpoint from {ckpt_path}...")
    with open(ckpt_path, "rb") as f:
        ckpt = pickle.load(f)

    feature_cols = ckpt["feature_cols"]
    X_train_imp = ckpt["X_train_imp"]
    y_train = ckpt["y_train"]
    X_holdout_imp = ckpt["X_holdout_imp"]
    y_holdout = ckpt["y_holdout"]
    best_lgb_params = ckpt["best_lgb_params"]

    # --- 1. Ablation Study ---
    print("\n--- 1. Running Ablation Study (4 Configurations) ---")
    feat_df_train = pd.DataFrame(X_train_imp, columns=feature_cols)
    feat_df_holdout = pd.DataFrame(X_holdout_imp, columns=feature_cols)

    # Define feature groups to ablate
    cart_features = [
        c for c in feature_cols if any(k in c.lower() for k in [
            "cart", "hesitation", "abandonment"
        ])
    ]
    trans_features = [
        c for c in feature_cols if any(k in c.lower() for k in [
            "trans", "spend", "order_value", "items", "purchase", "shipping"
        ])
    ]
    demo_features = [
        c for c in feature_cols if any(k in c.lower() for k in [
            "age", "tier", "loyalty", "credit", "income", "urban", "internet", "review", "referral"
        ])
    ]

    print(f"Total features: {len(feature_cols)}")
    print(f"Cart Engagement features ({len(cart_features)}): {cart_features}")
    print(f"Transaction features ({len(trans_features)}): {trans_features}")
    print(f"Demographic & Macro features ({len(demo_features)}): {demo_features}")

    ablation_configs = [
        ("Full Features", feature_cols),
        ("No Cart Engagement Features", [c for c in feature_cols if c not in cart_features]),
        ("No Historical Transaction Features", [c for c in feature_cols if c not in trans_features]),
        ("No Demographic Features", [c for c in feature_cols if c not in demo_features])
    ]

    ablation_results = []
    baseline_pr_auc = None

    for config_name, selected_cols in ablation_configs:
        t0 = time.time()
        X_tr = feat_df_train[selected_cols].values
        X_ho = feat_df_holdout[selected_cols].values

        clf = LGBMClassifier(**best_lgb_params)
        clf.fit(X_tr, y_train)
        probs = clf.predict_proba(X_ho)[:, 1]
        preds = (probs >= 0.5).astype(int)

        pr_auc = round(float(average_precision_score(y_holdout, probs)), 4)
        roc_auc = round(float(roc_auc_score(y_holdout, probs)), 4)
        f1 = round(float(f1_score(y_holdout, preds, zero_division=0)), 4)
        train_time = round(time.time() - t0, 2)

        if baseline_pr_auc is None:
            baseline_pr_auc = pr_auc
            drop_pct = 0.0
        else:
            drop_pct = round(((baseline_pr_auc - pr_auc) / baseline_pr_auc) * 100.0, 2)

        ablation_results.append({
            "feature_configuration": config_name,
            "features_count": len(selected_cols),
            "pr_auc": pr_auc,
            "pr_auc_drop_pct": drop_pct,
            "roc_auc": roc_auc,
            "f1_score": f1,
            "fit_time_sec": train_time
        })
        print(f"Config: {config_name} ({len(selected_cols)} feats) -> PR-AUC: {pr_auc} (Drop: {drop_pct}%), ROC-AUC: {roc_auc}")

    ablation_df = pd.DataFrame(ablation_results)
    ablation_csv = os.path.join(tables_dir, "tbl_ch4_ablation_study_results.csv")
    ablation_df.to_csv(ablation_csv, index=False)
    print(f"\nAblation study results saved to {ablation_csv}:")
    print(ablation_df.to_string(index=False))

    # --- 2. Multi-Seed Stability Testing ---
    print("\n--- 2. Running Multi-Seed Stability Testing (5 Seeds) ---")
    seeds = config["data_split"]["multi_seeds"]
    stability_records = []

    for seed in seeds:
        params = best_lgb_params.copy()
        params["random_state"] = seed
        clf = LGBMClassifier(**params)
        clf.fit(X_train_imp, y_train)

        probs = clf.predict_proba(X_holdout_imp)[:, 1]
        preds = (probs >= 0.5).astype(int)

        pr_auc = float(average_precision_score(y_holdout, probs))
        roc_auc = float(roc_auc_score(y_holdout, probs))
        brier = float(brier_score_loss(y_holdout, probs))
        f1 = float(f1_score(y_holdout, preds, zero_division=0))

        stability_records.append({
            "random_seed": seed,
            "pr_auc": round(pr_auc, 4),
            "roc_auc": round(roc_auc, 4),
            "brier_score": round(brier, 4),
            "f1_score": round(f1, 4)
        })
        print(f"Seed {seed}: PR-AUC={pr_auc:.4f}, ROC-AUC={roc_auc:.4f}, Brier={brier:.4f}")

    # Summary Row: Mean and Standard Deviation
    pr_aucs = [r["pr_auc"] for r in stability_records]
    roc_aucs = [r["roc_auc"] for r in stability_records]
    briers = [r["brier_score"] for r in stability_records]
    f1s = [r["f1_score"] for r in stability_records]

    stability_df = pd.DataFrame(stability_records)
    # Add summary row
    summary_row = pd.DataFrame([{
        "random_seed": "Mean ± Std",
        "pr_auc": f"{np.mean(pr_aucs):.4f} ± {np.std(pr_aucs):.4f}",
        "roc_auc": f"{np.mean(roc_aucs):.4f} ± {np.std(roc_aucs):.4f}",
        "brier_score": f"{np.mean(briers):.4f} ± {np.std(briers):.4f}",
        "f1_score": f"{np.mean(f1s):.4f} ± {np.std(f1s):.4f}"
    }])
    stability_final = pd.concat([stability_df, summary_row], ignore_index=True)

    stability_csv = os.path.join(tables_dir, "tbl_ch4_multiseed_stability.csv")
    stability_final.to_csv(stability_csv, index=False)
    print(f"\nMulti-Seed Stability results saved to {stability_csv}:")
    print(stability_final.to_string(index=False))

    gc.collect()


if __name__ == "__main__":
    run_ablation_and_stability()
