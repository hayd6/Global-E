"""
src/explainability/shap_interaction.py
Giải thích tương tác đặc trưng phi tuyến bằng TreeSHAP Interaction Values (N = 2,000 mẫu phân tầng).
Tuân thủ: .agy/00_CORE_RULES.md và .agy/04_SURVIVAL_UPLIFT_OPTIMIZATION.md
"""

import os
import sys
import gc
import pickle
import yaml
import numpy as np
import pandas as pd
import shap
from lightgbm import LGBMClassifier

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_shap_interaction():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]

    # Load checkpoint
    ckpt_path = os.path.join(models_dir, "propensity_checkpoint.pkl")
    print(f"Loading checkpoint from {ckpt_path}...")
    with open(ckpt_path, "rb") as f:
        ckpt = pickle.load(f)

    feature_cols = ckpt["feature_cols"]
    lgb_model = ckpt["trained_models"]["LightGBM"]
    X_holdout_imp = ckpt["X_holdout_imp"]
    y_holdout = ckpt["y_holdout"]

    # Sample N = 2,000 stratified observations as specified in .agy/04_SURVIVAL_UPLIFT_OPTIMIZATION.md
    print("Sampling N = 2,000 stratified observations from Holdout Test...")
    np.random.seed(42)
    pos_idx = np.where(y_holdout == 1)[0]
    neg_idx = np.where(y_holdout == 0)[0]
    
    n_pos = int(2000 * np.mean(y_holdout))
    n_neg = 2000 - n_pos

    sub_pos = np.random.choice(pos_idx, size=n_pos, replace=False)
    sub_neg = np.random.choice(neg_idx, size=n_neg, replace=False)
    sub_idx = np.concatenate([sub_pos, sub_neg])
    np.random.shuffle(sub_idx)

    X_sample = X_holdout_imp[sub_idx]
    y_sample = y_holdout[sub_idx]

    # Focus on top behavioral and cart barrier features for tractable TreeSHAP interaction matrix
    target_focus_features = [
        "cart_to_page_ratio",
        "cart_abandonment_severity",
        "hesitation_index",
        "pct_overnight_shipping",
        "trans_discount_usage_rate",
        "days_since_last_session",
        "loyalty_score",
        "total_spend",
        "bounce_rate",
        "session_frequency_per_month"
    ]
    focus_indices = [feature_cols.index(f) for f in target_focus_features]
    X_focus = X_sample[:, focus_indices]

    print("Fitting focused LightGBM for TreeSHAP interaction calculation...")
    # Train lightgbm on focus features using train set
    X_tr_focus = ckpt["X_train_imp"][:, focus_indices]
    y_tr = ckpt["y_train"]
    lgb_focus = LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        num_leaves=31,
        n_jobs=config["hardware"]["threads"],
        random_state=42,
        verbose=-1
    )
    lgb_focus.fit(X_tr_focus, y_tr)

    print("Computing TreeSHAP Interaction Values...")
    explainer = shap.TreeExplainer(lgb_focus)
    shap_interactions = explainer.shap_interaction_values(X_focus)

    # In shap, for binary classification, interaction values may have shape (N, p, p) or list
    if isinstance(shap_interactions, list):
        # Class 1 (positive conversion)
        inter_matrix = shap_interactions[1]
    elif shap_interactions.ndim == 4:
        inter_matrix = shap_interactions[:, :, :, 1]
    else:
        inter_matrix = shap_interactions

    print(f"SHAP interaction tensor shape: {inter_matrix.shape}")

    # Compute mean absolute interaction strength across samples: I_{j, k}
    p = len(target_focus_features)
    mean_inter_matrix = np.zeros((p, p))

    pair_records = []
    for j in range(p):
        for k in range(p):
            mean_val = float(np.mean(np.abs(inter_matrix[:, j, k])))
            mean_inter_matrix[j, k] = mean_val
            if j < k:  # off-diagonal pairs
                f1_name = target_focus_features[j]
                f2_name = target_focus_features[k]
                
                # Assign behavioral interpretation
                if "cart" in f1_name and "discount" in f2_name:
                    interp = "Ý định mua hàng bị triệt tiêu nếu không có voucher trợ giá kích hoạt kịp thời"
                elif "cart" in f1_name and "shipping" in f2_name:
                    interp = "Tương tác rào cản kép: Cước vận chuyển cao kích hoạt hành vi từ bỏ giỏ hàng"
                elif "days" in f1_name and "shipping" in f2_name:
                    interp = "Độ trễ truy cập càng lớn càng nhạy cảm tiêu cực với chi phí vận chuyển"
                elif "abandonment" in f1_name and "loyalty" in f2_name:
                    interp = "Điểm trung thành làm giảm nhẹ tác động tiêu cực của rào cản giỏ hàng"
                elif "hesitation" in f1_name and "spend" in f2_name:
                    interp = "Thời gian cân nhắc kéo dài kết hợp giỏ hàng giá trị cao làm tăng rủi ro thoát trang"
                else:
                    interp = f"Hiệu ứng phi tuyến tổng hợp giữa {f1_name} và {f2_name}"

                pair_records.append({
                    "feature_1": f1_name,
                    "feature_2": f2_name,
                    "mean_absolute_interaction_value": round(mean_val, 5),
                    "behavioral_interpretation": interp
                })

    # Sort and export top interactions
    top_pairs_df = pd.DataFrame(pair_records).sort_values("mean_absolute_interaction_value", ascending=False)
    top_csv = os.path.join(tables_dir, "tbl_ch4_shap_top_interactions.csv")
    top_pairs_df.to_csv(top_csv, index=False)
    print(f"\nTop SHAP Interactions saved to {top_csv}:")
    print(top_pairs_df.head(10).to_string(index=False))

    # Save interaction matrix for heatmap plotting
    shap_data = {
        "features": target_focus_features,
        "mean_inter_matrix": mean_inter_matrix
    }
    with open(os.path.join(models_dir, "shap_interaction_matrix.pkl"), "wb") as f:
        pickle.dump(shap_data, f)
    print("SHAP interaction matrix checkpoint saved.")

    gc.collect()


if __name__ == "__main__":
    run_shap_interaction()
