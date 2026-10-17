"""
src/business_value/plot_business_insights.py
Kết xuất 4 biểu đồ chuyên sâu chuẩn xuất bản học thuật (300 DPI, Tri-Color Palette):
1. fig_ch4_04_survival_cart_decay.png (Đường cong sống còn Kaplan-Meier phân tầng vận chuyển)
2. fig_ch4_05_uplift_qini_curve.png (Đường cong Qini của Uplift T-Learner)
3. fig_ch4_06_shap_interaction_matrix.png (Biểu đồ nhiệt tương tác phi tuyến SHAP)
4. fig_ch5_01_expected_profit_optimization.png (Đường cong tối ưu hóa lợi nhuận kinh tế kỳ vọng)
Tuân thủ: .agy/00_CORE_RULES.md và .agy/04_SURVIVAL_UPLIFT_OPTIMIZATION.md
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pickle
import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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


def plot_survival_decay(config, palette, figures_dir, models_dir):
    with open(os.path.join(models_dir, "kaplan_meier_fits.pkl"), "rb") as f:
        km_data = pickle.load(f)

    kmf_strata = km_data["kmf_strata"]
    kmf_global = km_data["kmf_global"]

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    strata_colors = {
        "Standard": "#0D9488",  # Forest Emerald
        "Express": "#2563EB",   # Royal Blue
        "Overnight": "#E11D48"  # Crimson Coral
    }

    t_grid = np.arange(1, 61)
    for cat, kmf in kmf_strata.items():
        surv_vals = [kmf.predict(t) for t in t_grid]
        color = strata_colors.get(cat, palette["primary"])
        ax.plot(t_grid, surv_vals, label=f"Vận chuyển: {cat}", color=color, linewidth=2.2)

    # Plot Golden Intervention Cutoff (t* = 7 days where slope decays rapidly)
    t_golden = 7
    ax.axvline(x=t_golden, color=palette["accent_warning"], linestyle="--", linewidth=1.8)

    ax.annotate(
        f"'Thời điểm vàng can thiệp': t* <= {t_golden} ngày\n(Tương tác tiếp thị phục hồi giỏ hàng\nphải thực hiện trước khi xác suất giảm sâu)",
        xy=(t_golden, 0.98),
        xytext=(t_golden + 4, 0.96),
        arrowprops=dict(
            facecolor=palette["accent_warning"],
            edgecolor=palette["accent_warning"],
            arrowstyle="->",
            lw=1.2
        ),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF1F2", edgecolor=palette["accent_warning"], alpha=0.9),
        fontsize=9.5,
        fontweight="bold",
        color=palette["primary"]
    )

    ax.set_xlabel("Thời gian trôi qua kể từ phiên gần nhất (Ngày)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_ylabel("Xác suất duy trì ý định mua hàng S(t)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title(
        "Đường cong sống còn Kaplan-Meier phân tầng theo phương thức vận chuyển",
        fontsize=13.5,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Mô hình hóa thời gian phân rã cơ hội của giỏ hàng | Dữ liệu Point-in-Time",
        fontsize=9.5,
        color="#475569",
        y=0.93
    )

    ax.legend(loc="lower left", fontsize=10, frameon=True, facecolor=palette["background"], edgecolor=palette["grid"])
    ax.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch4_04_survival_cart_decay.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_uplift_qini(config, palette, figures_dir, models_dir):
    with open(os.path.join(models_dir, "uplift_eval_data.pkl"), "rb") as f:
        uplift_data = pickle.load(f)

    qini_x = uplift_data["qini_x"]
    qini_y = uplift_data["qini_y"]
    random_qini = uplift_data["random_qini"]
    qini_score = uplift_data["qini_score"]

    fig, ax = plt.subplots(figsize=(9, 6.2), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    ax.plot(qini_x, qini_y, color=palette["accent_positive"], linewidth=2.5, label=f"Mô hình T-Learner (LightGBM)")
    ax.plot(qini_x, random_qini, color=palette["primary"], linestyle="--", linewidth=1.5, label="Phân bổ tiếp thị ngẫu nhiên (Random Line)")

    # Peak uplift callout
    peak_idx = int(np.argmax(qini_y))
    peak_x = qini_x[peak_idx]
    peak_y = qini_y[peak_idx]

    ax.scatter([peak_x], [peak_y], color=palette["accent_warning"], s=80, zorder=5)
    ax.annotate(
        f"Đỉnh gia tăng đơn hàng tích lũy\n(Tiếp cận Top {peak_x}% khách hàng Persuadables)",
        xy=(peak_x, peak_y),
        xytext=(peak_x + 8, peak_y - (abs(peak_y)*0.2 + 50)),
        arrowprops=dict(
            facecolor=palette["accent_warning"],
            edgecolor=palette["accent_warning"],
            arrowstyle="->",
            lw=1.2
        ),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF1F2", edgecolor=palette["accent_warning"], alpha=0.9),
        fontsize=9.5,
        fontweight="bold",
        color=palette["primary"]
    )

    ax.set_xlabel("Tỷ lệ dân số mục tiêu được can thiệp tiếp thị (%)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_ylabel("Số lượng đơn hàng gia tăng tích lũy (Qini Metric)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title(
        "Đường cong Qini đánh giá hiệu quả Uplift Modeling trên tập Holdout",
        fontsize=13.5,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Đo lường năng lực phân bổ ngân sách marketing vào đúng nhóm Persuadables | N = 32,000",
        fontsize=9.5,
        color="#475569",
        y=0.93
    )

    ax.legend(loc="lower right", fontsize=10, frameon=True, facecolor=palette["background"], edgecolor=palette["grid"])
    ax.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch4_05_uplift_qini_curve.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_shap_heatmap(config, palette, figures_dir, models_dir):
    with open(os.path.join(models_dir, "shap_interaction_matrix.pkl"), "rb") as f:
        shap_data = pickle.load(f)

    features = shap_data["features"]
    mat = shap_data["mean_inter_matrix"]

    # Shorten feature labels for visual clarity
    clean_labels = [
        f.replace("cart_to_page_ratio", "Cart/Page Ratio")
         .replace("cart_abandonment_severity", "Abandon Severity")
         .replace("hesitation_index", "Hesitation Index")
         .replace("pct_overnight_shipping", "Overnight Ship %")
         .replace("trans_discount_usage_rate", "Discount Rate")
         .replace("days_since_last_session", "Days Last Session")
         .replace("loyalty_score", "Loyalty Score")
         .replace("total_spend", "Total Spend")
         .replace("bounce_rate", "Bounce Rate")
         .replace("session_frequency_per_month", "Sessions/Month")
        for f in features
    ]

    fig, ax = plt.subplots(figsize=(10, 8.5), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    # Curated diverging colormap from background slate to emerald
    cmap = sns.light_palette(palette["accent_positive"], as_cmap=True)

    sns.heatmap(
        mat,
        xticklabels=clean_labels,
        yticklabels=clean_labels,
        annot=True,
        fmt=".3f",
        cmap=cmap,
        cbar_kws={"label": "Độ mạnh tương tác trung bình tuyệt đối (|SHAP Interaction|)"},
        linewidths=0.6,
        linecolor="#E2E8F0",
        ax=ax
    )

    ax.set_title(
        "Ma trận tương tác đặc trưng TreeSHAP (SHAP Interaction Values)",
        fontsize=13.5,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Bóc tách hiệu ứng phi tuyến giữa rào cản giỏ hàng và các yếu tố hành vi | N = 2,000",
        fontsize=9.5,
        color="#475569",
        y=0.93
    )

    plt.xticks(rotation=45, ha="right", fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)

    out_path = os.path.join(figures_dir, "fig_ch4_06_shap_interaction_matrix.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_expected_profit_curve(config, palette, figures_dir, models_dir):
    with open(os.path.join(models_dir, "profit_curve_data.pkl"), "rb") as f:
        data = pickle.load(f)

    df = data["thresh_df"]
    opt_tau = data["optimal_tau"]
    best_profit = data["best_profit"]
    def_tau = data["default_tau"]
    def_profit = data["default_profit"]
    delta_p = data["delta_profit"]

    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    ax.plot(df["threshold"], df["expected_net_profit_usd"] / 1000.0, color=palette["primary"], linewidth=2.5, label="Đường cong Lợi nhuận kinh tế kỳ vọng (Expected Profit Curve)")

    # Mark optimal threshold tau*
    ax.axvline(x=opt_tau, color=palette["accent_positive"], linestyle="--", linewidth=1.8, label=f"Ngưỡng tối ưu tau* = {opt_tau:.2f}")
    ax.scatter([opt_tau], [best_profit / 1000.0], color=palette["accent_positive"], s=100, zorder=5)

    # Mark default threshold 0.50
    ax.axvline(x=def_tau, color="#94A3B8", linestyle=":", linewidth=1.8, label=f"Ngưỡng mặc định tau = {def_tau:.2f}")
    ax.scatter([def_tau], [def_profit / 1000.0], color="#94A3B8", s=80, zorder=5)

    # Annotate gain
    ax.annotate(
        f"Điểm tối ưu tau* = {opt_tau:.2f}\nLợi nhuận ròng: ${best_profit:,.0f}\n(+${delta_p:,.0f} so với tau=0.50)",
        xy=(opt_tau, best_profit / 1000.0),
        xytext=(opt_tau + 0.12, (best_profit / 1000.0) * 0.85),
        arrowprops=dict(
            facecolor=palette["accent_positive"],
            edgecolor=palette["accent_positive"],
            arrowstyle="->",
            lw=1.4
        ),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#F0FDF4", edgecolor=palette["accent_positive"], alpha=0.9),
        fontsize=10,
        fontweight="bold",
        color=palette["primary"]
    )

    ax.set_xlabel("Ngưỡng xác suất quyết định can thiệp (Decision Threshold tau)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_ylabel("Lợi nhuận ròng kỳ vọng (Nghìn USD)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title(
        "Tối ưu hóa hàm lợi nhuận kinh tế kỳ vọng trên tập Holdout Test",
        fontsize=13.5,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Giả định: Biên lợi nhuận gộp 25% | Chi phí tiếp cận $1.0 | Chi phí voucher kích hoạt $5.0 | N = 32,000",
        fontsize=9.5,
        color="#475569",
        y=0.93
    )

    ax.legend(loc="upper right", fontsize=9.5, frameon=True, facecolor=palette["background"], edgecolor=palette["grid"])
    ax.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch5_01_expected_profit_optimization.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def main():
    config = load_config()
    palette = config["visual_standards"]["palette"]
    figures_dir = config["paths"]["figures_dir"]
    models_dir = config["paths"]["models_dir"]

    print("--- Plotting Business Insights and Optimization Figures ---")
    plot_survival_decay(config, palette, figures_dir, models_dir)
    plot_uplift_qini(config, palette, figures_dir, models_dir)
    plot_shap_heatmap(config, palette, figures_dir, models_dir)
    plot_expected_profit_curve(config, palette, figures_dir, models_dir)


if __name__ == "__main__":
    main()
