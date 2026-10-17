"""
src/models/uplift_modeling.py
Mô hình hóa tác động gia tăng của can thiệp tiếp thị (Uplift Modeling / CATE)
bằng kiến trúc Meta-Learner (T-Learner với LightGBM), phân loại 4 nhóm phản ứng kinh doanh,
và tính toán Qini Curve trên tập Holdout Test (32,000 dòng).
Tuân thủ: .agy/00_CORE_RULES.md và .agy/04_SURVIVAL_UPLIFT_OPTIMIZATION.md
"""

import os
import sys
import gc
import pickle
import yaml
import duckdb
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_uplift_modeling():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]
    experiments_dir = config["paths"]["experiments_dir"]
    feature_store_path = config["paths"]["feature_store_path"]

    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    n_jobs = config["hardware"]["threads"]
    random_state = config["data_split"]["random_state"]

    print("--- 1. Loading Data and Split Indices for Uplift Modeling ---")
    split_indices_path = os.path.join(experiments_dir, "split_indices.npz")
    splits = np.load(split_indices_path)
    train_idx = splits["train_indices"]
    holdout_idx = splits["holdout_indices"]

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

    # Define Treatment indicator W: Customer engaged via campaign or promotion
    # W = 1 if pct_campaign_sessions > 0 OR trans_discount_usage_rate > 0
    df["treatment"] = (
        (df["pct_campaign_sessions"] > 0) | (df["trans_discount_usage_rate"] > 0)
    ).astype(int)

    W = df["treatment"].values
    y = df["target"].values.astype(int)

    feature_cols = [c for c in df.columns if c not in ["target", "treatment"]]
    X = df[feature_cols].values

    # Impute missing with median
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy="median")
    X_imp = imputer.fit_transform(X)

    X_train, y_train, W_train = X_imp[train_idx], y[train_idx], W[train_idx]
    X_holdout, y_holdout, W_holdout = X_imp[holdout_idx], y[holdout_idx], W[holdout_idx]
    holdout_cust_ids = cust_ids[holdout_idx]

    n_treat_tr = np.sum(W_train == 1)
    n_ctrl_tr = np.sum(W_train == 0)
    print(f"Train Pool: Treatment (W=1) = {n_treat_tr:,} ({n_treat_tr/len(W_train)*100:.1f}%), Control (W=0) = {n_ctrl_tr:,} ({n_ctrl_tr/len(W_train)*100:.1f}%)")

    # --- 2. Train T-Learner (Two-Model Architecture) ---
    print("\n--- 2. Training T-Learner (LightGBM mu_1 and mu_0) ---")
    # Model 1: E[Y | X, W=1]
    model_t1 = LGBMClassifier(
        n_estimators=120,
        learning_rate=0.05,
        num_leaves=31,
        n_jobs=n_jobs,
        random_state=random_state,
        verbose=-1
    )
    model_t1.fit(X_train[W_train == 1], y_train[W_train == 1])

    # Model 0: E[Y | X, W=0]
    model_t0 = LGBMClassifier(
        n_estimators=120,
        learning_rate=0.05,
        num_leaves=31,
        n_jobs=n_jobs,
        random_state=random_state,
        verbose=-1
    )
    model_t0.fit(X_train[W_train == 0], y_train[W_train == 0])

    # --- 3. Predict Uplift (CATE) on Holdout Test ---
    print("\n--- 3. Estimating CATE and Classifying 4 Response Segments ---")
    mu_1_holdout = model_t1.predict_proba(X_holdout)[:, 1]
    mu_0_holdout = model_t0.predict_proba(X_holdout)[:, 1]
    tau_holdout = mu_1_holdout - mu_0_holdout

    print(f"Holdout Uplift Score Tau: Mean={np.mean(tau_holdout):.4f}, Min={np.min(tau_holdout):.4f}, Max={np.max(tau_holdout):.4f}")

    # Classify into 4 economic reaction segments:
    # 1. Persuadables: tau > 0 and above 60th percentile of tau
    # 2. Sleeping Dogs: tau < -0.01 (negative impact of marketing)
    # 3. Sure Things: mu_0 >= 0.25 (high organic probability) and tau in [-0.01, 0.05]
    # 4. Lost Causes: mu_1 < 0.25 and mu_0 < 0.25 and tau in [-0.01, 0.05]
    p65_tau = np.percentile(tau_holdout, 65)

    segments = []
    for i in range(len(y_holdout)):
        t_i = tau_holdout[i]
        m0_i = mu_0_holdout[i]
        m1_i = mu_1_holdout[i]

        if t_i > max(0.01, p65_tau):
            seg = "Persuadables"
        elif t_i < -0.005:
            seg = "Sleeping Dogs"
        elif m0_i >= 0.22:
            seg = "Sure Things"
        else:
            seg = "Lost Causes"
        segments.append(seg)

    seg_arr = np.array(segments)

    # Compile Segment Statistics
    seg_records = []
    for s_name in ["Persuadables", "Sure Things", "Lost Causes", "Sleeping Dogs"]:
        mask = (seg_arr == s_name)
        cnt = int(np.sum(mask))
        pct = round(cnt * 100.0 / len(seg_arr), 2)
        mean_tau = round(float(np.mean(tau_holdout[mask])), 4)
        
        # Empirical conversion rate in treatment vs control within segment
        tr_mask = mask & (W_holdout == 1)
        ctrl_mask = mask & (W_holdout == 0)
        tr_cr = round(float(np.mean(y_holdout[tr_mask])) * 100.0, 2) if np.sum(tr_mask) > 0 else 0.0
        ctrl_cr = round(float(np.mean(y_holdout[ctrl_mask])) * 100.0, 2) if np.sum(ctrl_mask) > 0 else 0.0
        net_inc = int(np.sum(tau_holdout[mask] * cnt))

        recs = {
            "Persuadables": "Ưu tiên số 1: Can thiệp voucher và tiếp thị cá thể hóa cao",
            "Sure Things": "Cấm cấp voucher; bảo toàn 100% biên lợi nhuận tự nhiên",
            "Lost Causes": "Loại bỏ khỏi chiến dịch; tránh lãng phí chi phí tiếp cận",
            "Sleeping Dogs": "Tuyệt đối không can thiệp; tránh phản cảm gây mất khách hàng"
        }

        seg_records.append({
            "uplift_segment": s_name,
            "customer_count": cnt,
            "pct_population": pct,
            "mean_uplift_score": mean_tau,
            "treatment_conversion_rate": tr_cr,
            "control_conversion_rate": ctrl_cr,
            "net_incremental_orders": net_inc,
            "business_recommendation": recs[s_name]
        })

    seg_df = pd.DataFrame(seg_records)
    seg_csv = os.path.join(tables_dir, "tbl_ch4_uplift_segments_summary.csv")
    seg_df.to_csv(seg_csv, index=False)
    print(f"\nUplift segments summary saved to {seg_csv}:")
    print(seg_df[["uplift_segment", "customer_count", "pct_population", "mean_uplift_score", "treatment_conversion_rate", "control_conversion_rate"]].to_string(index=False))

    # --- 4. Compute Qini Metric and Qini Curve ---
    print("\n--- 4. Computing Qini Curve and Qini Score ---")
    # Sort Holdout by predicted Uplift Tau descending
    sorted_indices = np.argsort(-tau_holdout)
    y_sorted = y_holdout[sorted_indices]
    W_sorted = W_holdout[sorted_indices]

    n_bins = 100
    bin_size = len(y_holdout) // n_bins
    qini_x = []
    qini_y = []
    cum_nt = 0
    cum_nc = 0
    cum_yt = 0
    cum_yc = 0

    total_nt = np.sum(W_holdout == 1)
    total_nc = np.sum(W_holdout == 0)

    for b in range(1, n_bins + 1):
        idx_range = sorted_indices[:b * bin_size]
        sub_y = y_holdout[idx_range]
        sub_w = W_holdout[idx_range]

        n_t = np.sum(sub_w == 1)
        n_c = np.sum(sub_w == 0)
        y_t = np.sum(sub_y[sub_w == 1])
        y_c = np.sum(sub_y[sub_w == 0])

        # Qini formula: Y_t - Y_c * (N_t / N_c)
        if n_c > 0:
            q_val = y_t - (y_c * (n_t / (n_c + 1e-6)))
        else:
            q_val = y_t

        qini_x.append(b)  # Percentage of population targeted
        qini_y.append(float(q_val))

    # Random baseline line: linearly from 0 to total qini
    random_qini = [float(qini_y[-1] * (x / 100.0)) for x in qini_x]
    
    # Qini Score: Area between Qini curve and random line
    try:
        from scipy.integrate import trapezoid
        qini_score = float(trapezoid(qini_y, qini_x) - trapezoid(random_qini, qini_x))
    except Exception:
        qini_score = float(np.trapezoid(qini_y, qini_x) - np.trapezoid(random_qini, qini_x))
    print(f"Qini Score (Area under Uplift vs Random): {qini_score:.2f}")

    # Save Uplift Evaluation Data for plotting and Power BI export
    uplift_eval_data = {
        "qini_x": qini_x,
        "qini_y": qini_y,
        "random_qini": random_qini,
        "qini_score": qini_score,
        "holdout_cust_ids": holdout_cust_ids,
        "tau_holdout": tau_holdout,
        "mu_1_holdout": mu_1_holdout,
        "mu_0_holdout": mu_0_holdout,
        "segments_holdout": seg_arr
    }
    with open(os.path.join(models_dir, "uplift_eval_data.pkl"), "wb") as f:
        pickle.dump(uplift_eval_data, f)

    # Save full customer uplift score predictions (200,000 customers) for Power BI Fact table
    print("Generating full population Uplift predictions for Power BI...")
    con_full = duckdb.connect()
    full_df = con_full.execute(f"SELECT customer_id FROM '{feature_store_path}' ORDER BY customer_id").df()
    full_X = con_full.execute(f"SELECT * EXCLUDE (customer_id, target) FROM '{feature_store_path}' ORDER BY customer_id").df()[feature_cols].values
    con_full.close()
    full_X_imp = imputer.transform(full_X)
    
    full_mu_1 = model_t1.predict_proba(full_X_imp)[:, 1]
    full_mu_0 = model_t0.predict_proba(full_X_imp)[:, 1]
    full_tau = full_mu_1 - full_mu_0
    
    full_p65 = np.percentile(full_tau, 65)
    full_segs = []
    for t_val, m0_val, m1_val in zip(full_tau, full_mu_0, full_mu_1):
        if t_val > max(0.01, full_p65):
            full_segs.append("Persuadables")
        elif t_val < -0.005:
            full_segs.append("Sleeping Dogs")
        elif m0_val >= 0.22:
            full_segs.append("Sure Things")
        else:
            full_segs.append("Lost Causes")

    full_uplift_df = pd.DataFrame({
        "customer_id": full_df["customer_id"],
        "uplift_score": full_tau.astype(np.float32),
        "uplift_segment": full_segs
    })
    full_uplift_df.to_parquet(os.path.join(config["paths"]["processed_data_dir"], "customer_uplift_scores.parquet"), index=False, compression="snappy")
    print("Full population uplift predictions saved.")

    gc.collect()


if __name__ == "__main__":
    run_uplift_modeling()
