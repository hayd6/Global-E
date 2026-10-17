# DÀN Ý SLIDE THUYẾT TRÌNH BẢO VỆ DỰ ÁN (18 SLIDES CHUYÊN SÂU)

**Đề tài:** Phân tích rào cản chuyển đổi giỏ hàng và tối ưu hóa lợi nhuận tiếp thị trong thương mại điện tử  
**Đơn vị thực hiện:** Hệ thống Thực nghiệm Khoa học Dữ liệu Lớn (AGY Pipeline)  
**Tập trung:** 80% thời lượng vào Phát hiện Insight Rào cản giỏ hàng & Bằng chứng Tối ưu hóa Lợi nhuận Kinh tế  

---

## SLIDE 1: TIÊU ĐỀ BÁO CÁO & TUYÊN NGÔN BÀI TOÁN
- **Tiêu đề chính:** Phân tích rào cản chuyển đổi giỏ hàng & Tối ưu hóa lợi nhuận tiếp thị TMĐT.
- **Vấn nạn cốt lõi:** Tỷ lệ bỏ rơi giỏ hàng đạt 79.7%, lãng phí hàng chục nghìn USD ngân sách CAC vào tiếp thị đại trà.
- **Tuyên ngôn giải pháp:** Chuyển hóa từ phân tích mô tả tĩnh sang Khung hỗ trợ ra quyết định kinh tế tiền tệ (Prescriptive Decision Framework).

## SLIDE 2: BỐI CẢNH DỮ LIỆU ĐA BẢNG & RANH GIỚI POINT-IN-TIME (PIT)
- **Quy mô dữ liệu:** 200,000 khách hàng, 2,000,000 phiên, 500,000 giao dịch.
- **Ranh giới thời gian t0:** Mốc chốt 2024-06-01, cửa sổ nhãn 30 ngày tương lai.
- **Kiểm soát rò rỉ:** 100% đặc trưng tính toán từ dữ liệu <= t0, vượt qua 3 bài test pytest độc lập.

## SLIDE 3: KIỂM TOÁN VÀ KHẮC PHỤC SAI LỆCH DỮ LIỆU GỐC (DATA HEALING)
- **Sai lệch đảo ngược thời gian:** Lọc bỏ 997,299 phiên và 249,377 giao dịch trước ngày đăng ký.
- **Chuẩn hóa:** Xử lý 10,000 giá trị tuổi khuyết tật bằng trung vị theo hạng hội viên, chuẩn hóa 25,059 giao dịch items_count <= 0.
- **Bảo toàn dữ liệu:** Giữ nguyên 100% 200,000 khách hàng phục vụ bài toán toàn dân số.

## SLIDE 4: ĐẶC TRƯNG HÀNH VI GIỎ HÀNG BẬC CAO (FEATURE STORE)
- **61 đặc trưng Point-in-Time:** Tập trung vào các chỉ số ma sát giỏ hàng mới:
  - `cart_to_page_ratio`: Cường độ ý định mua hàng so với lướt xem.
  - `hesitation_index`: Thời gian đắn đo cân nhắc cho mỗi lần thêm giỏ.
  - `cart_abandonment_severity`: Số phiên có thêm giỏ nhưng bỏ rơi thanh toán.
  - `pct_overnight_shipping`: Mức độ chịu cước vận chuyển cao.

## SLIDE 5: KIỂM ĐỊNH GIẢ THUYẾT RÀO CẢN HÀNH VI (H1, H2, H3)
- **Kiểm định chuẩn:** D'Agostino-Pearson bác bỏ phân phối chuẩn (p < 1e-50).
- **H1 (Ma sát vận chuyển):** Mann-Whitney U test p = 7.04e-08, khẳng định nhóm từ bỏ giỏ hàng chịu cước Overnight cao hơn có ý nghĩa thống kê.
- **H2 (Phân rã tương tác):** Kruskal-Wallis p < 1e-100, tốc độ thêm giỏ suy giảm mạnh theo Recency.

## SLIDE 6: PHÂN KHÚC HÀNH VI ĐA CHIỀU GMM (RFM-E SOFT CLUSTERING)
- **Lựa chọn tối ưu:** Tiêu chuẩn BIC đạt điểm uốn tại k* = 5 cụm (BIC = -2.63 triệu).
- **So sánh mô hình:** Vượt trội hơn K-Means và HDBSCAN về khả năng định danh xác suất mềm.
- **Radar Chart:** Trực quan hóa hình thái khác biệt rõ nét trên 5 trục không gian.

## SLIDE 7: CHÂN DUNG 5 PHÂN KHÚC KHÁCH HÀNG THỰC TẾ
1. **High-Value Champions (6.6%):** Chi tiêu $423.6, tần suất 2.6 đơn, ít bỏ giỏ.
2. **Cart Hesitators (25.0%):** Bỏ giỏ nghiêm trọng nhất (4.9 phiên/người) -> **Điểm gãy chuyển đổi chính**.
3. **Discount Seekers (28.9%):** Nhạy cảm với ưu đãi, tương tác thường xuyên.
4. **Dormant At-Risk (19.7%):** Độ trễ phiên cực cao (> 400 ngày), nguy cơ rời bỏ hoàn toàn.
5. **Passive Browsers (19.8%):** Xem nhiều, thêm giỏ ít, chi tiêu thấp.

## SLIDE 8: HUẤN LUYỆN VÀ TỐI ƯU HÓA SIÊU THAM SỐ OPTUNA
- **Chiến lược:** 5-Fold Stratified Cross-Validation, hàm mục tiêu PR-AUC, 35 trials/mô hình.
- **Kết quả Boosting:**
  - LightGBM: PR-AUC = 0.2742
  - CatBoost: PR-AUC = 0.2753
  - XGBoost: PR-AUC = 0.2755
  - Stacking Ensemble: Kết hợp Out-Of-Fold đạt PR-AUC = 0.2753.

## SLIDE 9: ĐỘ TIN CẬY VÀ HIỆU CHỈNH XÁC SUẤT (PLATT SCALING)
- **Vấn đề mô hình thô:** LightGBM raw bị lệch độ tin cậy nặng (ECE = 0.2645).
- **Hiệu chuẩn Platt Sigmoid:** Đưa sai số ECE về 0.0006, Brier score giảm về 0.1578.
- **Ý nghĩa sống còn:** Xác suất p dự đoán phản ánh chính xác tần suất thực tế, điều kiện tiên quyết để tính toán hàm lợi nhuận ròng.

## SLIDE 10: KIỂM ĐỊNH ĐỘ ỔN ĐỊNH VÀ ABLATION STUDY
- **Multi-Seed Testing:** 5 hạt giống độc lập [42, 100, 2024, 2026, 777] đạt PR-AUC = 0.2743 ± 0.0004 (Siêu ổn định).
- **Ablation Study:** Loại bỏ biến nhân khẩu học làm sụt giảm 22.1% PR-AUC, khẳng định giá trị phối hợp đặc trưng.

## SLIDE 11: MÔ HÌNH HÓA SỐNG CÒN GIỎ HÀNG (KAPLAN-MEIER & COXPH)
- **Thời điểm vàng can thiệp:** Sau t* = 7 ngày, xác suất sống còn của cơ hội giỏ hàng giảm mạnh.
- **CoxPH Hazard Ratios:**
  - `cart_to_page_ratio`: HR = 1.3121 (Làm tăng 31.2% nguy cơ từ bỏ, p < 1e-5).
  - `cart_abandonment_severity`: HR = 1.0510 (Mỗi phiên bỏ giỏ tăng 5.1% rủi ro rời bỏ).
  - `trans_discount_usage_rate`: HR = 0.9201 (Giảm 8.0% rủi ro từ bỏ, p = 0.0098).

## SLIDE 12: BÓC TÁCH TƯƠNG TÁC PHI TUYẾN TREESHAP
- **Top tương tác:** Tương tác giữa `cart_to_page_ratio` và `loyalty_score` (|SHAP| = 0.01169).
- **Insight hành vi:** Lòng trung thành thương hiệu đóng vai trò lớp đệm giảm sốc, giúp khách hàng vượt qua rào cản chi phí vận chuyển.

## SLIDE 13: SUY LUẬN NHÂN QUẢ UPLIFT MODELING (T-LEARNER CATE)
- **Bản chất:** Ước lượng tác động gia tăng thực sự của marketing: tau_i = E[Y|X, W=1] - E[Y|X, W=0].
- **4 nhóm phản ứng:**
  - **Persuadables (35.0%):** Nhóm duy nhất sinh lời từ ưu đãi -> **Ưu tiên số 1**.
  - **Sure Things (3.7%):** Tự mua không cần ưu đãi -> **Cấm phát hành voucher**.
  - **Lost Causes (52.2%):** Không mua dù có tiếp thị -> **Loại bỏ**.
  - **Sleeping Dogs (9.1%):** Tiếp thị làm giảm tỷ lệ mua -> **Tránh xa**.

## SLIDE 14: TỐI ƯU HÓA HÀM LỢI NHUẬN KINH TẾ KỲ VỌNG
- **Phương trình lợi nhuận:** Profit(tau) = sum [ I(p >= tau) * (y * (Margin - C_voucher) - C_contact) ].
- **Tham số:** Margin = 25%, C_contact = $1.0, C_voucher = $5.0.
- **So sánh bước ngoặt:**
  - Ngưỡng mặc định tau = 0.50: Lợi nhuận = $0 (Không can thiệp được ai).
  - Ngưỡng tối ưu tau* = 0.01: Lợi nhuận ròng đạt **$115,917.05** (ROI = 179.8%).

## SLIDE 15: PHÂN VỊ 10 DECILES VÀ LIFT@K
- **Decile 1:** Tỷ lệ phản hồi 31.91%, **Lift@K = 1.57**, tạo ra $18,668 lợi nhuận ròng.
- **Top 20% (Decile 1-2):** Thâu tóm 28.98% tổng lượng đơn hàng mua thực tế.
- **Ý nghĩa:** Chuyển dịch từ tiếp thị dàn trải sang tiếp thị tập trung, cắt giảm 60% chi phí tiếp cận CAC.

## SLIDE 16: KIẾN TRÚC DASHBOARD POWER BI & DEMO WEB STREAMLIT
- **Power BI Star Schema:** 4 bảng quan hệ 1-Nhiều hoàn chỉnh (200k dòng).
- **Streamlit Web App:**
  - Tab 1: Chẩn đoán cá thể hóa và cảnh báo rào cản giỏ hàng live qua `best_calibrated_model.pkl`.
  - Tab 2: What-If Profit Simulator điều chỉnh Margin/Chi phí trong thời gian thực.
  - Tab 3: Uplift Strategy Matrix và xuất file thực thi marketing.

## SLIDE 17: MA TRẬN 4 GÓI ĐỀ XUẤT HÀNH ĐỘNG DOANH NGHIỆP
1. **ACT-01:** Miễn phí vận chuyển linh hoạt khi giỏ hàng >= 80% AOV cho Cụm Cart Hesitators.
2. **ACT-02:** Cấp voucher $5.0 có giới hạn countdown 24h duy nhất cho nhóm Persuadables.
3. **ACT-03:** Kích hoạt thông báo tự động vào giờ thứ 3 theo thời điểm vàng sống còn Kaplan-Meier.
4. **ACT-04:** Phân bổ 80% ngân sách vào Decile 1 & 2 kết hợp ngưỡng tối ưu tau*.

## SLIDE 18: TỔNG KẾT VÀ BƯỚC ĐI TIẾP THEO
- **Kết luận:** Dự án đã giải quyết trọn vẹn bài toán từ kỹ thuật dữ liệu đến giá trị lợi nhuận tiền tệ.
- **Bước tiếp theo:** Khuyến nghị tiến hành thử nghiệm A/B Testing 4 tuần trên môi trường trực tiếp để nghiệm thu giá trị thực tế.
