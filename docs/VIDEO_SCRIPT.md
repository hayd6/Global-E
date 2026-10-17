# KỊCH BẢN VIDEO DEMO VÀ BẢO VỆ DỰ ÁN (THỜI LƯỢNG 3–5 PHÚT)

**Tên đề tài:** Phân tích rào cản chuyển đổi giỏ hàng và tối ưu hóa lợi nhuận tiếp thị trong thương mại điện tử  
**Mục tiêu video:** Giới thiệu ngắn gọn vấn đề rào cản giỏ hàng, trình diễn hệ thống phân tích dữ liệu lớn và demo trực tiếp ứng dụng Streamlit hỗ trợ ra quyết định kinh tế.

---

### PHẦN 1: ĐẶT VẤN ĐỀ VÀ BỐI CẢNH DỰ ÁN (00:00 – 00:45)
- **Hình ảnh trình chiếu:** Slide 1 & Slide 2. Biểu đồ phân phối nhãn mất cân bằng 3.9:1 (`fig_ch3_01_target_distribution.png`).
- **Lời thuyết minh:**  
  *"Kính thưa Hội đồng, trong thương mại điện tử, 79.7% khách hàng sau khi thêm sản phẩm vào giỏ hàng đã từ bỏ mà không thanh toán. Cách tiếp cận truyền thống là phát voucher giảm giá đại trà, vừa gây lãng phí ngân sách vừa không giải quyết được các điểm gãy ma sát hành vi cốt lõi.  
  Dự án của chúng tôi xây dựng một Khung phân tích hỗ trợ ra quyết định kinh tế hoàn chỉnh trên 200,000 khách hàng và 2,000,000 phiên truy cập, tuân thủ nghiêm ngặt nguyên tắc Point-in-Time để loại bỏ 100% rò rỉ dữ liệu."*

---

### PHẦN 2: PHÁT HIỆN INSIGHT RÀO CẢN VÀ MÔ HÌNH HÓA (00:45 – 01:45)
- **Hình ảnh trình chiếu:** Biểu đồ Radar GMM (`fig_ch3_03_gmm_cluster_radar.png`), Đường cong sống còn Kaplan-Meier (`fig_ch4_04_survival_cart_decay.png`) và Ma trận tương tác TreeSHAP (`fig_ch4_06_shap_interaction_matrix.png`).
- **Lời thuyết minh:**  
  *"Qua kiểm định phi tham số Mann-Whitney U và phân khúc Gaussian Mixture Models, chúng tôi phát hiện nhóm 'Cart Hesitators' chiếm 25% dân số nhưng bỏ giỏ trung bình tới 4.9 phiên do rào cản chi phí giao hàng Overnight.  
  Phân tích sống còn Kaplan-Meier và mô hình CoxPH chỉ ra thời điểm vàng can thiệp là trong 7 ngày đầu, với nguy cơ từ bỏ giỏ hàng tăng 31.2% nếu tỷ lệ cart-to-page cao.  
  Đặc biệt, mô hình Uplift T-Learner đã bóc tách chính xác 35% khách hàng thuộc nhóm Persuadables – đây là đối tượng duy nhất mang lại chuyển đổi gia tăng thuần từ ưu đãi, trong khi nhóm Sure Things chiếm 3.7% tự mua mà không cần voucher."*

---

### PHẦN 3: DEMO TƯƠNG TÁC ỨNG DỤNG WEB STREAMLIT (01:45 – 03:15)
- **Thao tác màn hình:** Mở trình duyệt tại ứng dụng Streamlit `app/app.py`.
- **Thao tác Tab 1 (Chẩn đoán cá thể hóa):**
  - Nhập khách hàng: 18 trang xem, 6 lượt thêm giỏ, thời lượng 450s, cước Overnight.
  - Bấm Chẩn đoán: Hệ thống gọi trực tiếp `best_calibrated_model.pkl` (Platt Sigmoid với ECE = 0.0006).
  - **Lời thuyết minh:** *"Hệ thống cảnh báo rào cản giỏ hàng nghiêm trọng do cước Overnight và tự động đề xuất cấp voucher trợ cước $5.0 trước giờ thứ 3 cho nhóm Persuadables."*
- **Thao tác Tab 2 (What-If Profit Simulator):**
  - Kéo thanh trượt Margin từ 25% lên 35%, điều chỉnh chi phí tiếp cận $C_contact = $1.0, voucher = $5.0.
  - **Lời thuyết minh:** *"Đường cong Expected Profit Curve tự động vẽ lại trong thời gian thực, cho thấy ngưỡng tối ưu tau* dịch chuyển linh hoạt, tối đa hóa lợi nhuận đạt hơn $115,000 trên tập Holdout, vượt trội hoàn toàn so với ngưỡng mặc định 0.50."*
- **Thao tác Tab 3 (Chiến lược Uplift):**
  - Bấm nút tải danh sách khách hàng Persuadables xuất file CSV.
  - **Lời thuyết minh:** *"Hệ thống sẵn sàng trích xuất danh sách khách hàng mục tiêu để tích hợp thẳng vào nền tảng Marketing Automation."*

---

### PHẦN 4: KẾT LUẬN GIÁ TRỊ KINH DOANH VÀ NGHIỆM THU (03:15 – 04:00)
- **Hình ảnh trình chiếu:** Bảng 10 Deciles Lift@K (`tbl_ch5_decile_lift_profit.csv`) và Ma trận hành động (`tbl_ch5_business_action_matrix.csv`).
- **Lời thuyết minh:**  
  *"Nhờ tiếp cận dựa trên giá trị kinh tế kỳ vọng và xếp hạng Decile Lift@K, doanh nghiệp có thể tập trung 80% ngân sách vào Top 20% khách hàng có Lift đạt 1.57, giúp giảm 60% chi phí CAC mà vẫn thâu tóm gần 30% tổng lượng đơn hàng.  
  Toàn bộ dự án đã được đóng gói thành công với 4 bảng Star Schema Power BI, Ứng dụng Streamlit, Báo cáo Word 6 phần chi tiết và mã nguồn điều phối tự động 1-click `run_pipeline.py`.  
  Xin chân thành cảm ơn Hội đồng đã chú ý lắng nghe!"*
