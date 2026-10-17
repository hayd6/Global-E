"""
src/data_engineering/plot_pit_audit.py
Kết xuất biểu đồ kiểm toán phân phối nhãn và rào cản giỏ hàng
Tuân thủ: .agy/00_CORE_RULES.md và .agy/01_DATA_ENGINEERING_PIT.md
Quy chuẩn: 300 DPI, Tri-Color Palette, despine, lưới mờ alpha=0.3
"""

import os
import yaml
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_style(palette):
    plt.rcParams["font.sans-serif"] = "Arial, DejaVu Sans, Helvetica"
    plt.rcParams["axes.edgecolor"] = palette["primary"]
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["figure.facecolor"] = palette["background"]
    plt.rcParams["axes.facecolor"] = palette["background"]


def plot_target_distribution(con, config, palette, figures_dir):
    df = con.execute("""
        SELECT 
            target, 
            COUNT(*) as count, 
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () as pct
        FROM 'data/processed/customer_features_pit.parquet'
        WHERE target IS NOT NULL
        GROUP BY target
        ORDER BY target
    """).df()

    fig, ax = plt.subplots(figsize=(8, 6), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    labels = ["Không chuyển đổi (Target = 0)", "Chuyển đổi mua hàng (Target = 1)"]
    counts = df["count"].values
    pcts = df["pct"].values
    colors = [palette["accent_warning"], palette["accent_positive"]]

    bars = ax.bar(labels, counts, color=colors, width=0.52, edgecolor=palette["primary"], linewidth=1.2, zorder=3)

    for bar, count, pct in zip(bars, counts, pcts):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 2500,
            f"{count:,.0f} khách hàng\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=palette["primary"]
        )

    ax.set_ylim(0, max(counts) * 1.18)
    ax.set_ylabel("Số lượng khách hàng", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title(
        "Phân phối nhãn chuyển đổi giỏ hàng (Mất cân bằng 3.9 : 1)",
        fontsize=14,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Cửa sổ quan sát nhãn: 30 ngày sau mốc chốt t0 (2024-06-01 đến 2024-07-01) | N = 160,000",
        fontsize=9.5,
        color="#475569",
        y=0.92
    )

    ax.grid(axis="y", linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"], zorder=0)
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch3_01_target_distribution.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def plot_cart_engagement_scatter(con, config, palette, figures_dir):
    # Sample 8,000 observations for crisp visual representation
    df = con.execute("""
        SELECT 
            total_pages_viewed, 
            total_cart_additions, 
            target
        FROM 'data/processed/customer_features_pit.parquet'
        WHERE target IS NOT NULL
        USING SAMPLE 8000 (reservoir, 42)
    """).df()

    fig, ax = plt.subplots(figsize=(10, 7), dpi=config["visual_standards"]["dpi"])
    setup_style(palette)

    # Plot Target = 0 (Abandonment) first, then Target = 1 (Conversion)
    df_neg = df[df["target"] == 0]
    df_pos = df[df["target"] == 1]

    ax.scatter(
        df_neg["total_pages_viewed"],
        df_neg["total_cart_additions"],
        c=palette["accent_warning"],
        label="Từ bỏ giỏ hàng (Target = 0)",
        alpha=0.45,
        s=26,
        edgecolors="none",
        zorder=2
    )
    ax.scatter(
        df_pos["total_pages_viewed"],
        df_pos["total_cart_additions"],
        c=palette["accent_positive"],
        label="Chuyển đổi thành công (Target = 1)",
        alpha=0.65,
        s=30,
        edgecolors="none",
        zorder=3
    )

    # Highlight Friction Zone: High pages viewed, high cart additions, yet no conversion
    p90_pages = float(np.percentile(df["total_pages_viewed"], 65))
    p75_cart = float(np.percentile(df["total_cart_additions"], 65))

    ax.axvline(x=p90_pages, color=palette["accent_warning"], linestyle="--", alpha=0.7, linewidth=1.2)
    ax.axhline(y=p75_cart, color=palette["accent_warning"], linestyle="--", alpha=0.7, linewidth=1.2)

    ax.annotate(
        "Vùng ma sát giỏ hàng nghiêm trọng\n(Duyệt nhiều trang, thêm giỏ nhiều\nnhưng không chuyển đổi)",
        xy=(p90_pages * 1.25, p75_cart * 1.3),
        xytext=(p90_pages * 1.5, p75_cart * 1.7),
        arrowprops=dict(
            facecolor=palette["primary"],
            edgecolor=palette["primary"],
            arrowstyle="->",
            lw=1.2
        ),
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF1F2", edgecolor=palette["accent_warning"], alpha=0.9),
        fontsize=10,
        fontweight="bold",
        color=palette["primary"]
    )

    ax.set_xlabel("Tổng số trang đã xem (Total Pages Viewed)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_ylabel("Tổng số lượt thêm vào giỏ (Total Cart Additions)", fontsize=11, fontweight="bold", color=palette["primary"])
    ax.set_title(
        "Mối liên hệ giữa tương tác duyệt trang và ý định thêm vào giỏ hàng",
        fontsize=14,
        fontweight="bold",
        pad=16,
        color=palette["primary"]
    )
    plt.suptitle(
        "Dữ liệu Point-in-Time tại t0 (2024-06-01) | Mẫu đại diện ngẫu nhiên N = 8,000",
        fontsize=9.5,
        color="#475569",
        y=0.93
    )

    ax.legend(frameon=True, facecolor=palette["background"], edgecolor=palette["grid"], fontsize=10, loc="upper left")
    ax.grid(True, linestyle="--", alpha=config["visual_standards"]["grid_alpha"], color=palette["grid"])
    sns.despine(top=True, right=True)

    out_path = os.path.join(figures_dir, "fig_ch3_02_cart_engagement_scatter.png")
    plt.savefig(out_path, dpi=config["visual_standards"]["dpi"], bbox_inches="tight")
    plt.close()
    print(f"Exported: {out_path}")


def main():
    config = load_config()
    palette = config["visual_standards"]["palette"]
    figures_dir = config["paths"]["figures_dir"]
    os.makedirs(figures_dir, exist_ok=True)

    con = duckdb.connect()
    con.execute(f"SET threads = {config['hardware']['threads']};")
    con.execute(f"SET max_memory = '{config['hardware']['duckdb_max_memory']}';")

    print("--- Plotting PIT Audit Figures ---")
    plot_target_distribution(con, config, palette, figures_dir)
    plot_cart_engagement_scatter(con, config, palette, figures_dir)
    con.close()


if __name__ == "__main__":
    main()
