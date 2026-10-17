"""
src/models/plot_model_evaluation.py
Kết xuất 3 biểu đồ đánh giá mô hình học máy đạt chuẩn đồ họa học thuật (300 DPI, Tri-Color Palette):
1. fig_ch4_01_roc_pr_curves_comparison.png (ROC & PR curves)
2. fig_ch4_02_calibration_curves.png (Reliability Diagram & Distribution)
3. fig_ch4_03_ablation_study_bar.png (Ablation Study Drop Bar Chart)
Tuân thủ: .agy/00_CORE_RULES.md và .agy/03_PROPENSITY_AND_CALIBRATION.md
"""

import os
import sys
import pickle
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score, average_precision_score
from sklearn.calibration import calibration_curve

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_style(palette):
    plt.rcParams["font.sans-serif"] = "Arial, DejaVu Sans, Helvetica"
    plt.rcParams["axes.edgecolor"] = palette["primary"]
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["figure.facecolor"] = palette["background"]
    plt.rcParams["axes.facecolor"] = palette["background"]


def plot_roc_pr_comparison(config, palette, figures_dir, models_dir):
    with open(os.path.join(models_dir, "holdout_predictions.pkl"), "rb") as f:
        data = pickle.load(f)

    y_true = data["y_holdout"]
    probs = data["probs"]

    fig, (ax_roc, ax_pr) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    model_colors = {
        "Calibrated LightGBM (Platt Sigmoid)": ("#0D9488", "-", 2.5),  # Forest Emerald
        "LightGBM": ("#2563EB", "--", 1.8),                           # Royal Blue
        "CatBoost": ("#7C3AED", "-.", 1.8),                           # Purple
        "XGBoost": ("#D97706", ":", 1.8),                             # Amber
        "Random Forest": ("#64748B", "-", 1.4),                        # Slate
        "Logistic Regression": ("#94A3B8", "--", 1.4)                 # Light Slate
    }

    # Left: ROC Curves
    for m_name, (color, ls, lw) in model_colors.items():
        if m_name in probs:
            p = probs[m_name]
            fpr, tpr, _ = roc_curve(y_true, p)
            auc_val = roc_auc_score(y_true, p)
            display_name = m_name.replace("Calibrated LightGBM (Platt Sigmoid)", "Calibrated LightGBM")
            ax_roc.plot(fpr, tpr, label=f"{display_name} (AUC = {auc_val:.3f})", color=color, linestyle=ls, linewidth=lw)

    ax_roc.plot([0, 1], [0, 1], "k--", alpha=0.3, linewidth=1.0, label="Random Chance (0.500)")
    ax_roc.set_xlabel("Tỷ lệ dương tính giả (False Positive Rate)", fontsize=10.5, fontweight="bold", color=palette["primary"])
    ax_roc.set_ylabel("Tỷ lệ dương tính thật (True Positive Rate)", fontsize=10.5, fontweight="bold", color=palette["primary"])
    ax_roc.set_title("Đường cong ROC (Receiver Operating Characteristic)", fontsize=12.5, fontweight="bold", color=palette["primary"])
    ax_roc.legend(loc="lower right", fontsize=8.5, frameon=True, facecolor=palette["background"], edgecolor=palette["grid"])
    ax_roc.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(ax=ax_roc, top=True, right=True)

    # Right: Precision-Recall Curves
    baseline_pr = float(np.mean(y_true))
    for m_name, (color, ls, lw) in model_colors.items():
        if m_name in probs:
            p = probs[m_name]
            prec, rec, _ = precision_recall_curve(y_true, p)
            pr_auc_val = average_precision_score(y_true, p)
            display_name = m_name.replace("Calibrated LightGBM (Platt Sigmoid)", "Calibrated LightGBM")
            ax_pr.plot(rec, prec, label=f"{display_name} (PR-AUC = {pr_auc_val:.3f})", color=color, linestyle=ls, linewidth=lw)

    ax_pr.axhline(y=baseline_pr, color="#E11D48", linestyle=":", label=f"Tỷ lệ cơ sở (No-Skill = {baseline_pr:.3f})", linewidth=1.2)
    ax_pr.set_xlabel("Độ nhạy thu hồi (Recall)", fontsize=10.5, fontweight="bold", color=palette["primary"])
    ax_pr.set_ylabel("Độ chuẩn xác (Precision)", fontsize=10.5, fontweight="bold", color=palette["primary"])
    ax_pr.set_title("Đường cong Precision-Recall (Đánh giá trên tập mất cân bằng)", fontsize=12.5, fontweight="bold", color=palette["primary"])
    ax_pr.legend(loc="upper right", fontsize=8.5, frameon=True, facecolor=palette["background"], edgecolor=palette["grid"])
    ax_pr.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(ax=ax_pr, top=True, right=True)

    plt.suptitle("So sánh năng lực phân loại của 6 mô hình trên tập Holdout Test (N = 32,000)", fontsize=14, fontweight="bold", color=palette["primary"], y=0.98)
    out_path = os.path.join(figures_dir, "fig_ch4_01_roc_pr_curves_comparison.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_calibration_curves(config, palette, figures_dir, models_dir):
    with open(os.path.join(models_dir, "calibration_eval_data.pkl"), "rb") as f:
        calib_data = pickle.load(f)

    y_true = calib_data["y_holdout"]
    lgb_p = calib_data["lgbm_prob"]
    iso_p = calib_data["iso_prob"]
    sig_p = calib_data["sig_prob"]

    fig = plt.figure(figsize=(9, 8), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    # Subplot grid: 3 rows (top 2 for calibration curve, bottom 1 for probability histogram)
    gs = fig.add_gridspec(3, 1, hspace=0.28)
    ax_curve = fig.add_subplot(gs[0:2, 0])
    ax_hist = fig.add_subplot(gs[2, 0])

    # Plot 45-degree reference line
    ax_curve.plot([0, 1], [0, 1], "k:", label="Chuẩn hoàn hảo (Perfect Calibration)", linewidth=1.5)

    # Calibration curves (10 bins)
    prob_true_raw, prob_pred_raw = calibration_curve(y_true, lgb_p, n_bins=10, strategy="uniform")
    prob_true_iso, prob_pred_iso = calibration_curve(y_true, iso_p, n_bins=10, strategy="uniform")
    prob_true_sig, prob_pred_sig = calibration_curve(y_true, sig_p, n_bins=10, strategy="uniform")

    ax_curve.plot(prob_pred_raw, prob_true_raw, "s-", color="#E11D48", linewidth=2.0, label="Chưa hiệu chỉnh (LightGBM Raw, ECE=0.265)")
    ax_curve.plot(prob_pred_iso, prob_true_iso, "o-", color="#2563EB", linewidth=2.0, label="Isotonic Calibration (ECE=0.002)")
    ax_curve.plot(prob_pred_sig, prob_true_sig, "^-", color="#0D9488", linewidth=2.5, label="Platt Scaling / Sigmoid (ECE=0.0006 - Tối ưu)")

    ax_curve.set_ylabel("Tần suất chuyển đổi thực tế", fontsize=10.5, fontweight="bold", color=palette["primary"])
    ax_curve.set_title("Đường cong hiệu chỉnh độ tin cậy xác suất (Reliability Diagram)", fontsize=13, fontweight="bold", color=palette["primary"], pad=12)
    ax_curve.legend(loc="upper left", fontsize=9, frameon=True, facecolor=palette["background"], edgecolor=palette["grid"])
    ax_curve.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(ax=ax_curve, top=True, right=True)

    # Histogram of calibrated probabilities
    ax_hist.hist(sig_p, bins=25, color=palette["primary"], alpha=0.8, edgecolor=palette["background"], density=True)
    ax_hist.set_xlabel("Xác suất dự đoán sau hiệu chỉnh (Predicted Probability)", fontsize=10.5, fontweight="bold", color=palette["primary"])
    ax_hist.set_ylabel("Mật độ phân phối", fontsize=10, fontweight="bold", color=palette["primary"])
    ax_hist.grid(axis="y", linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(ax=ax_hist, top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch4_02_calibration_curves.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_ablation_bar(config, palette, figures_dir, tables_dir):
    ablation_csv = os.path.join(tables_dir, "tbl_ch4_ablation_study_results.csv")
    df = pd.read_csv(ablation_csv)

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    # Sort configs for nice bar chart
    labels = df["feature_configuration"].tolist()[::-1]
    pr_aucs = df["pr_auc"].tolist()[::-1]
    drops = df["pr_auc_drop_pct"].tolist()[::-1]

    colors = [
        palette["accent_warning"] if d > 1.0 else ("#2563EB" if d > 0.0 else palette["accent_positive"])
        for d in drops
    ]

    bars = ax.barh(labels, pr_aucs, color=colors, height=0.48, edgecolor=palette["primary"], linewidth=1.1, zorder=3)

    for bar, val, drop in zip(bars, pr_aucs, drops):
        w = bar.get_width()
        drop_text = f" (Suy giảm {drop:.1f}%)" if drop > 0.05 else " (Cơ sở chuẩn)"
        ax.text(
            w + 0.005,
            bar.get_y() + bar.get_height() / 2.0,
            f"{val:.4f}{drop_text}",
            va="center",
            ha="left",
            fontsize=9.5,
            fontweight="bold",
            color=palette["primary"]
        )

    ax.set_xlim(0, max(pr_aucs) * 1.35)
    ax.set_xlabel("Chỉ số PR-AUC trên tập Holdout Test (N = 32,000)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title("Mức độ suy giảm hiệu năng qua nghiên cứu triệt tiêu (Ablation Study)", fontsize=13.5, fontweight="bold", color=palette["primary"], pad=14)
    plt.suptitle("Đánh giá vai trò đóng góp thông tin của từng nhóm đặc trưng", fontsize=9.5, color="#475569", y=0.92)

    ax.grid(axis="x", linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"], zorder=0)
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch4_03_ablation_study_bar.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def main():
    config = load_config()
    palette = config["visual_standards"]["palette"]
    figures_dir = config["paths"]["figures_dir"]
    models_dir = config["paths"]["models_dir"]
    tables_dir = config["paths"]["tables_dir"]

    print("--- Plotting Model Evaluation Figures ---")
    plot_roc_pr_comparison(config, palette, figures_dir, models_dir)
    plot_calibration_curves(config, palette, figures_dir, models_dir)
    plot_ablation_bar(config, palette, figures_dir, tables_dir)


if __name__ == "__main__":
    main()
