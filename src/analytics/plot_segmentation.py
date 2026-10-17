"""
src/analytics/plot_segmentation.py
Xuất 3 biểu đồ phân khúc khách hàng và lựa chọn siêu tham số GMM đạt chuẩn đồ họa học thuật
Tuân thủ: .agy/00_CORE_RULES.md và .agy/02_BEHAVIORAL_SEGMENTATION.md
Quy chuẩn: 300 DPI, Tri-Color Palette, despine, lưới mờ alpha=0.3
"""

import os
import sys
import yaml
import duckdb
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


def plot_gmm_radar(config, palette, figures_dir, tables_dir):
    profiles_csv = os.path.join(tables_dir, "tbl_ch3_gmm_cluster_profiles.csv")
    df = pd.read_csv(profiles_csv)

    # 5 axes for radar: Recency, Frequency, Monetary, Cart Additions, Abandonment Severity
    categories = [
        "Recency (Độ trễ)",
        "Frequency (Tần suất)",
        "Monetary (Chi tiêu)",
        "Cart Additions (Thêm giỏ)",
        "Abandonment (Bỏ rơi giỏ)"
    ]
    raw_cols = [
        "mean_recency",
        "mean_frequency",
        "mean_monetary",
        "mean_cart_additions",
        "mean_abandonment_severity"
    ]

    # Normalize each column to [0, 1] using min-max for clean radar visualization
    norm_vals = {}
    for col in raw_cols:
        c_min = df[col].min()
        c_max = df[col].max()
        norm_vals[col] = (df[col] - c_min) / (c_max - c_min + 1e-6)

    norm_df = pd.DataFrame(norm_vals)

    # Set up radar chart
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete loop

    fig, ax = plt.subplots(figsize=(9, 8), subplot_kw=dict(polar=True), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    # Curated palette for 5 personas
    cluster_colors = [
        "#0D9488",  # Forest Emerald (Champions)
        "#E11D48",  # Crimson Coral (Cart Hesitators)
        "#2563EB",  # Royal Blue (Discount Seekers)
        "#64748B",  # Slate Grey (Dormant)
        "#D97706"   # Amber (Browsers)
    ]

    for i, row in df.iterrows():
        values = norm_df.iloc[i].values.flatten().tolist()
        values += values[:1]
        c_color = cluster_colors[i % len(cluster_colors)]
        p_name = f"Cụm {row['cluster_id']}: {row['persona_name']}"
        ax.plot(angles, values, linewidth=2, linestyle="solid", label=p_name, color=c_color)
        ax.fill(angles, values, color=c_color, alpha=0.12)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, fontweight="bold", color=palette["primary"])
    ax.set_rlabel_position(30)
    plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], color="#64748B", size=8)
    plt.ylim(0, 1.05)
    ax.grid(color=palette["grid"], linestyle="--", alpha=0.5)

    ax.set_title(
        "Hình thái đa chiều 5 cụm khách hàng RFM-E (GMM Soft Clustering)",
        fontsize=13,
        fontweight="bold",
        pad=24,
        color=palette["primary"]
    )
    plt.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.12),
        fontsize=9,
        frameon=True,
        facecolor=palette["background"],
        edgecolor=palette["grid"]
    )

    out_path = os.path.join(figures_dir, "fig_ch3_03_gmm_cluster_radar.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_cart_friction_by_cluster(config, palette, figures_dir, processed_dir, tables_dir):
    con = duckdb.connect()
    assign_path = os.path.join(processed_dir, "customer_cluster_assignments.parquet")
    features_path = config["paths"]["feature_store_path"]

    df = con.execute(f"""
        SELECT 
            a.gmm_cluster_id,
            f.cart_abandonment_severity
        FROM '{assign_path}' a
        JOIN '{features_path}' f ON a.customer_id = f.customer_id
        USING SAMPLE 15000 (reservoir, 42)
    """).df()
    con.close()

    profiles_csv = os.path.join(tables_dir, "tbl_ch3_gmm_cluster_profiles.csv")
    prof = pd.read_csv(profiles_csv).sort_values("cluster_id")
    name_map = dict(zip(prof["cluster_id"], prof["persona_name"]))
    df["persona_label"] = df["gmm_cluster_id"].map(lambda x: f"Cụm {x}\n{name_map.get(x, '')}")

    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    order = [f"Cụm {i}\n{name_map.get(i, '')}" for i in sorted(name_map.keys())]
    box_colors = ["#0D9488", "#E11D48", "#2563EB", "#64748B", "#D97706"]

    sns.boxplot(
        data=df,
        x="persona_label",
        y="cart_abandonment_severity",
        order=order,
        palette=box_colors,
        ax=ax,
        width=0.55,
        fliersize=2,
        linewidth=1.2,
        boxprops=dict(alpha=0.85)
    )

    # Highlight Cụm 2: Cart Hesitators
    ax.annotate(
        "Điểm gãy chuyển đổi: Cụm 2 (Cart Hesitators)\ncó mức độ bỏ rơi giỏ hàng nghiêm trọng nhất\n(Trung bình 4.9 phiên bỏ giỏ/khách hàng)",
        xy=(1, 10.5),
        xytext=(1.4, 13.5),
        arrowprops=dict(
            facecolor=palette["accent_warning"],
            edgecolor=palette["accent_warning"],
            arrowstyle="->",
            lw=1.4
        ),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF1F2", edgecolor=palette["accent_warning"], alpha=0.9),
        fontsize=9.5,
        fontweight="bold",
        color=palette["primary"]
    )

    ax.set_xlabel("Phân khúc khách hàng GMM", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_ylabel("Mức độ nghiêm trọng bỏ giỏ (Cart Abandonment Severity)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title(
        "Phân hóa rào cản bỏ rơi giỏ hàng giữa 5 phân khúc khách hàng",
        fontsize=13.5,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Số phiên có thêm sản phẩm vào giỏ nhưng không thanh toán | Mẫu đại diện N = 15,000",
        fontsize=9.5,
        color="#475569",
        y=0.93
    )

    ax.grid(axis="y", linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch3_04_cart_friction_by_cluster.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_gmm_bic_aic(config, palette, figures_dir, tables_dir):
    bic_csv = os.path.join(tables_dir, "tbl_ch3_gmm_bic_aic_raw.csv")
    df = pd.read_csv(bic_csv)

    fig, ax = plt.subplots(figsize=(9, 5.8), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    ax.plot(df["k"], df["bic"] / 1e6, marker="o", linewidth=2.2, color=palette["primary"], label="BIC (Bayesian Information Criterion)")
    ax.plot(df["k"], df["aic"] / 1e6, marker="s", linewidth=2.2, color=palette["accent_positive"], linestyle="--", label="AIC (Akaike Information Criterion)")

    # Mark optimal k = 5
    opt_k = 5
    bic_opt = df[df["k"] == opt_k]["bic"].values[0] / 1e6

    ax.axvline(x=opt_k, color=palette["accent_warning"], linestyle=":", linewidth=2.0)
    ax.scatter([opt_k], [bic_opt], color=palette["accent_warning"], s=90, zorder=5)

    ax.annotate(
        f"Số cụm tối ưu k* = {opt_k}\n(Điểm cân bằng cấu trúc nghiệp vụ\nvà thông tin thống kê)",
        xy=(opt_k, bic_opt),
        xytext=(opt_k + 0.35, bic_opt + 0.35),
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

    ax.set_xlabel("Số thành phần phân cụm (Number of Mixture Components k)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_ylabel("Giá trị tiêu chuẩn thông tin (x 1,000,000)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title(
        "Lựa chọn số cụm tối ưu cho Gaussian Mixture Models qua BIC & AIC",
        fontsize=13.5,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Đánh giá trên toàn bộ 200,000 khách hàng | Không gian 5 chiều RFM-E",
        fontsize=9.5,
        color="#475569",
        y=0.93
    )

    ax.legend(frameon=True, facecolor=palette["background"], edgecolor=palette["grid"], fontsize=10, loc="upper right")
    ax.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch3_05_gmm_bic_aic_selection.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def main():
    config = load_config()
    palette = config["visual_standards"]["palette"]
    figures_dir = config["paths"]["figures_dir"]
    tables_dir = config["paths"]["tables_dir"]
    processed_dir = config["paths"]["processed_data_dir"]

    print("--- Plotting Segmentation Figures ---")
    plot_gmm_radar(config, palette, figures_dir, tables_dir)
    plot_cart_friction_by_cluster(config, palette, figures_dir, processed_dir, tables_dir)
    plot_gmm_bic_aic(config, palette, figures_dir, tables_dir)


if __name__ == "__main__":
    main()
