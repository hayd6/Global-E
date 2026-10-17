"""
src/business_value/profit_optimization.py
Tối ưu hóa lợi nhuận kinh tế kỳ vọng (Expected Profit Optimization) quét ngưỡng tau in [0.01, 0.99]
và lập bảng hiệu năng phân vị 10 Deciles với Lift@K trên tập Holdout Test (32,000 dòng).
Tuân thủ: .agy/00_CORE_RULES.md và .agy/04_SURVIVAL_UPLIFT_OPTIMIZATION.md
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import gc
import pickle
import yaml
import duckdb
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from src.models.pipeline_wrapper import FullPipelineModel

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_profit_optimization():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    models_dir = config["paths"]["models_dir"]
    experiments_dir = config["paths"]["experiments_dir"]
    feature_store_path = config["paths"]["feature_store_path"]

    os.makedirs(tables_dir, exist_ok=True)

    # Economic assumptions
    margin_rate = config["business_assumptions"]["gross_margin_rate"]  # 0.25
    c_contact = config["business_assumptions"]["contact_cost_usd"]      # 1.0
    c_voucher = config["business_assumptions"]["voucher_cost_usd"]      # 5.0
    default_tau = config["business_assumptions"]["default_threshold"]   # 0.50
    step = config["business_assumptions"]["threshold_scan_step"]        # 0.01

    print("--- 1. Loading Best Calibrated Model and Holdout Data ---")
    with open(os.path.join(models_dir, "best_calibrated_model.pkl"), "rb") as f:
        best_model = pickle.load(f)

    split_indices_path = os.path.join(experiments_dir, "split_indices.npz")
    splits = np.load(split_indices_path)
    holdout_idx = splits["holdout_indices"]

    con = duckdb.connect()
    holdout_df = con.execute(f"""
        SELECT 
            customer_id,
            target,
            avg_order_value,
            total_spend,
            trans_count
        FROM '{feature_store_path}'
        WHERE target IS NOT NULL
        ORDER BY customer_id
    """).df().iloc[holdout_idx].copy()
    
    full_holdout_features = con.execute(f"""
        SELECT * EXCLUDE (customer_id, target)
        FROM '{feature_store_path}'
        WHERE target IS NOT NULL
        ORDER BY customer_id
    """).df().iloc[holdout_idx].copy()
    con.close()

    # Predict calibrated probability on Holdout
    print("Generating calibrated probabilities on Holdout Test...")
    p_holdout = best_model.predict_proba(full_holdout_features)[:, 1]
    y_holdout = holdout_df["target"].values.astype(int)

    # Calculate customer margin: Margin_i = 0.25 * AOV_i
    # If customer has 0 past transactions, impute median AOV of transactors (~$85)
    valid_aov = holdout_df[holdout_df["avg_order_value"] > 0]["avg_order_value"]
    median_aov = float(valid_aov.median()) if len(valid_aov) > 0 else 85.0
    
    customer_aov = np.where(holdout_df["avg_order_value"] > 0, holdout_df["avg_order_value"], median_aov)
    customer_margin = margin_rate * customer_aov

    print(f"Customer Margin: Median=${np.median(customer_margin):.2f}, Mean=${np.mean(customer_margin):.2f}")

    # --- 2. Threshold Scanning: tau in [0.01, 0.99] ---
    print("\n--- 2. Scanning Thresholds tau in [0.01, 0.99] for Expected Profit Optimization ---")
    thresholds = np.arange(0.01, 1.00, step)
    threshold_records = []

    best_profit = -np.inf
    optimal_tau = 0.50

    for tau in thresholds:
        tau = round(float(tau), 2)
        targeted = (p_holdout >= tau).astype(int)
        n_contacts = int(np.sum(targeted))

        if n_contacts > 0:
            tp = int(np.sum((targeted == 1) & (y_holdout == 1)))
            fp = int(np.sum((targeted == 1) & (y_holdout == 0)))
            
            # Profit formula: sum [ targeted_i * (y_i * (Margin_i - c_voucher) - c_contact) ]
            profit = float(np.sum(targeted * (y_holdout * (customer_margin - c_voucher) - c_contact)))
            total_cost = float((n_contacts * c_contact) + (tp * c_voucher))
            roi = (profit / total_cost) * 100.0 if total_cost > 0 else 0.0

            prec = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
            rec = float(tp / np.sum(y_holdout)) if np.sum(y_holdout) > 0 else 0.0
            f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        else:
            tp, fp = 0, 0
            profit = 0.0
            total_cost = 0.0
            roi = 0.0
            prec, rec, f1 = 0.0, 0.0, 0.0

        if profit > best_profit:
            best_profit = profit
            optimal_tau = tau

        threshold_records.append({
            "threshold": tau,
            "total_contacts": n_contacts,
            "true_positives": tp,
            "false_positives": fp,
            "expected_net_profit_usd": round(profit, 2),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roi_percentage": round(roi, 2)
        })

    thresh_df = pd.DataFrame(threshold_records)
    thresh_csv = os.path.join(tables_dir, "tbl_ch5_threshold_optimization_results.csv")
    thresh_df.to_csv(thresh_csv, index=False)
    print(f"Threshold simulation saved to {thresh_csv}")

    # Baseline profit at default threshold tau = 0.50
    default_row = thresh_df[thresh_df["threshold"] == default_tau].iloc[0]
    optimal_row = thresh_df[thresh_df["threshold"] == optimal_tau].iloc[0]

    delta_profit = optimal_row["expected_net_profit_usd"] - default_row["expected_net_profit_usd"]
    profit_gain_pct = (delta_profit / abs(default_row["expected_net_profit_usd"])) * 100.0 if default_row["expected_net_profit_usd"] != 0 else np.nan

    print("\n--- ECONOMIC OPTIMIZATION COMPARISON ---")
    print(f"Optimal Threshold tau*: {optimal_tau:.2f}")
    print(f"Profit at tau*: ${optimal_row['expected_net_profit_usd']:,.2f} (Contacts: {optimal_row['total_contacts']:,}, ROI: {optimal_row['roi_percentage']:.1f}%)")
    print(f"Profit at Default tau=0.50: ${default_row['expected_net_profit_usd']:,.2f} (Contacts: {default_row['total_contacts']:,}, ROI: {default_row['roi_percentage']:.1f}%)")
    print(f"Net Profit Gain: +${delta_profit:,.2f} (+{profit_gain_pct:.1f}%)")

    # Save threshold summary for plotting
    with open(os.path.join(models_dir, "profit_curve_data.pkl"), "wb") as f:
        pickle.dump({
            "thresh_df": thresh_df,
            "optimal_tau": optimal_tau,
            "best_profit": best_profit,
            "default_tau": default_tau,
            "default_profit": default_row["expected_net_profit_usd"],
            "delta_profit": delta_profit
        }, f)

    # --- 3. Decile Lift@K Table ---
    print("\n--- 3. Constructing 10-Decile Lift and Cumulative Profit Table ---")
    holdout_df["pred_prob"] = p_holdout
    holdout_df["customer_margin"] = customer_margin
    holdout_df = holdout_df.sort_values("pred_prob", ascending=False).reset_index(drop=True)

    n_total = len(holdout_df)
    n_pos_total = np.sum(y_holdout)
    overall_response_rate = n_pos_total / n_total

    decile_records = []
    decile_size = n_total // 10

    cum_pos = 0
    cum_contacts = 0
    cum_profit = 0.0

    for d in range(1, 11):
        start_i = (d - 1) * decile_size
        end_i = d * decile_size if d < 10 else n_total
        sub_d = holdout_df.iloc[start_i:end_i]

        n_k = len(sub_d)
        y_k = int(sub_d["target"].sum())
        resp_rate = y_k / n_k
        lift_k = resp_rate / overall_response_rate

        cum_pos += y_k
        cum_contacts += n_k
        cum_recall = cum_pos / n_pos_total
        precision_at_k = cum_pos / cum_contacts

        # Profit generated within decile d
        decile_profit = float(np.sum(
            sub_d["target"].values * (sub_d["customer_margin"].values - c_voucher) - c_contact
        ))
        cum_profit += decile_profit

        decile_records.append({
            "decile": d,
            "customer_count": n_k,
            "actual_purchases": y_k,
            "response_rate_pct": round(resp_rate * 100.0, 2),
            "lift_at_k": round(lift_k, 2),
            "cumulative_recall_pct": round(cum_recall * 100.0, 2),
            "precision_at_k_pct": round(precision_at_k * 100.0, 2),
            "decile_net_profit_usd": round(decile_profit, 2),
            "cumulative_net_profit_usd": round(cum_profit, 2)
        })

    decile_df = pd.DataFrame(decile_records)
    decile_csv = os.path.join(tables_dir, "tbl_ch5_decile_lift_profit.csv")
    decile_df.to_csv(decile_csv, index=False)
    print(f"\nDecile Lift & Profit saved to {decile_csv}:")
    print(decile_df.to_string(index=False))

    gc.collect()


if __name__ == "__main__":
    run_profit_optimization()
