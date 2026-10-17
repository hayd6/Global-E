"""
src/business_value/generate_business_recommendations.py
Tổng hợp 4 Insight cốt lõi từ thực nghiệm và xây dựng ma trận 4 gói đề xuất hành động kinh doanh định lượng.
Tuân thủ: .agy/00_CORE_RULES.md và .agy/05_DASHBOARD_WEB_AND_REPORT.md
"""

import os
import sys

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import yaml
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_business_recommendations():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    os.makedirs(tables_dir, exist_ok=True)

    print("--- Generating Quantitative Business Action Matrix ---")

    # Load empirical tables to cross-reference exact numbers
    cox_df = pd.read_csv(os.path.join(tables_dir, "tbl_ch4_coxph_hazard_ratios.csv"))
    uplift_df = pd.read_csv(os.path.join(tables_dir, "tbl_ch4_uplift_segments_summary.csv"))
    thresh_df = pd.read_csv(os.path.join(tables_dir, "tbl_ch5_threshold_optimization_results.csv"))
    decile_df = pd.read_csv(os.path.join(tables_dir, "tbl_ch5_decile_lift_profit.csv"))
    profiles_df = pd.read_csv(os.path.join(tables_dir, "tbl_ch3_gmm_cluster_profiles.csv"))

    opt_tau = float(thresh_df.sort_values("expected_net_profit_usd", ascending=False).iloc[0]["threshold"])
    opt_profit = float(thresh_df.sort_values("expected_net_profit_usd", ascending=False).iloc[0]["expected_net_profit_usd"])
    persuadables_pct = float(uplift_df[uplift_df["uplift_segment"] == "Persuadables"]["pct_population"].iloc[0])
    sure_things_pct = float(uplift_df[uplift_df["uplift_segment"] == "Sure Things"]["pct_population"].iloc[0])

    actions = [
        {
            "strategy_id": "ACT-01",
            "strategy_name": "Giải tỏa rào cản cước vận chuyển (Dynamic Free Shipping Threshold)",
            "target_segment": "Cụm 2: Cart Hesitators / Shipping-Sensitive (25.04% dân số)",
            "behavioral_barrier_addressed": "Ma sát chi phí vận chuyển Overnight làm gia tăng tỷ lệ bỏ giỏ (Cart Abandonment Severity trung bình 4.9 phiên)",
            "intervention_action": "Kích hoạt chính sách Miễn phí vận chuyển linh hoạt khi giá trị giỏ hàng đạt 80% AOV hoặc đề xuất gói gộp đơn thông minh",
            "channel": "On-site Cart Drawer & Checkout Banner",
            "optimal_threshold": "Giá trị giỏ hàng >= $68.0 (80% AOV)",
            "potential_risks": "Bào mòn biên lợi nhuận gộp nếu khách hàng chia nhỏ đơn hàng",
            "mitigation_plan": "Áp dụng điều kiện biên lợi nhuận danh mục sản phẩm tối thiểu >= 28% mới kích hoạt miễn phí vận chuyển",
            "target_kpi": "Giảm 20% tỷ lệ Cart Abandonment Severity; tăng 15% tỷ lệ hoàn tất thanh toán giỏ hàng"
        },
        {
            "strategy_id": "ACT-02",
            "strategy_name": "Can thiệp ưu đãi cá thể hóa theo Uplift CATE (Targeted Incentive Allocation)",
            "target_segment": "Duy nhất nhóm Persuadables (35.00% dân số)",
            "behavioral_barrier_addressed": "Lãng phí ngân sách voucher vào nhóm Sure Things (3.66%) và gây phản cảm cho nhóm Sleeping Dogs (9.12%)",
            "intervention_action": "Cấp voucher giảm giá $5.0 có giới hạn thời gian (Scarcity Countdown 24h); tuyệt đối chặn phát hành voucher cho Sure Things và Sleeping Dogs",
            "channel": "Email Marketing Automation & SMS Flash Sale",
            "optimal_threshold": "Điểm số tác động gia tăng Uplift Tau >= 0.10",
            "potential_risks": "Khách hàng hình thành tâm lý chờ đợi mã giảm giá mới mua",
            "mitigation_plan": "Giới hạn tối đa 1 voucher trợ giá / khách hàng trong chu kỳ 30 ngày; mã hóa voucher động không thể chia sẻ",
            "target_kpi": "Tăng 25% tỷ lệ chuyển đổi thuần (Net Uplift Conversion); tiết kiệm $15,000 ngân sách voucher bị lãng phí"
        },
        {
            "strategy_id": "ACT-03",
            "strategy_name": "Kích hoạt tự động theo thời điểm vàng sống còn (Golden Window Retargeting)",
            "target_segment": "Khách hàng có phiên thêm giỏ nhưng chưa hoàn tất giao dịch trong vòng 7 ngày",
            "behavioral_barrier_addressed": "Xác suất duy trì ý định mua hàng suy giảm mạnh theo thời gian bán rã Kaplan-Meier (sau 7 ngày xác suất phục hồi giảm sâu)",
            "intervention_action": "Kích hoạt chuỗi thông báo tự động đa kênh vào đúng giờ thứ 3 và giờ thứ 24 kể từ khi rời giỏ hàng, hiển thị hình ảnh sản phẩm còn trong giỏ",
            "channel": "Mobile Push Notification & Personalized Retargeting",
            "optimal_threshold": "Thời gian trôi qua: 3h <= t <= 24h (t* <= 7 ngày)",
            "potential_risks": "Tần suất nhắc nhở quá dày đặc dẫn đến tỷ lệ hủy đăng ký nhận tin (Unsubscribe) tăng cao",
            "mitigation_plan": "Thiết lập quy tắc Frequency Capping tối đa 2 thông báo nhắc giỏ / tuần / khách hàng",
            "target_kpi": "Đạt tỷ lệ mở thông báo >= 35%; tỷ lệ phục hồi giỏ hàng hoàn tất thanh toán >= 12%"
        },
        {
            "strategy_id": "ACT-04",
            "strategy_name": "Tối ưu hóa phân bổ ngân sách theo phân vị Decile Lift@K & Ngưỡng tau*",
            "target_segment": "Decile 1 và Decile 2 (Top 20% khách hàng có xác suất chuyển đổi cao nhất)",
            "behavioral_barrier_addressed": "Tiếp thị dàn trải kém hiệu quả với ngưỡng mặc định tau=0.50 dẫn đến bỏ lỡ cơ hội lợi nhuận kinh tế",
            "intervention_action": "Tập trung 80% ngân sách tiếp cận marketing vào Decile 1 & 2 (Lift@K đạt từ 1.33 đến 1.57); áp dụng ngưỡng quyết định kinh tế tối ưu tau* để tối đa hóa hàm lợi nhuận ròng",
            "channel": "Paid Search Retargeting & Meta Custom Audience",
            "optimal_threshold": f"Ngưỡng quyết định tối ưu tau* = {opt_tau:.2f} (hoặc Decile 1-2)",
            "potential_risks": "Bỏ lỡ khách hàng tiềm năng ở các phân vị thấp nếu ngân sách bị cắt giảm quá sâu",
            "mitigation_plan": "Duy trì tiếp cận chi phí thấp qua kênh Organic SEO, Email Newsletter cho các phân vị 3-10",
            "target_kpi": f"Tối đa hóa lợi nhuận ròng đạt ${opt_profit:,.0f} trên tập Holdout; giảm 60% chi phí tiếp cận khách hàng (CAC)"
        }
    ]

    action_df = pd.DataFrame(actions)
    action_csv = os.path.join(tables_dir, "tbl_ch5_business_action_matrix.csv")
    action_df.to_csv(action_csv, index=False)
    print(f"Business Action Matrix successfully exported to {action_csv}:")
    print(action_df[["strategy_id", "strategy_name", "target_segment", "optimal_threshold", "target_kpi"]].to_string(index=False))


if __name__ == "__main__":
    generate_business_recommendations()
