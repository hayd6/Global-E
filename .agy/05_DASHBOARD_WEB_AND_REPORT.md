# .agy/05_DASHBOARD_WEB_AND_REPORT.md

## GIAI ĐOẠN 5: XUẤT DỮ LIỆU STAR-SCHEMA CHO POWER BI, WEB APP THỰC TẾ, TỔNG HỢP INSIGHT & ĐỀ XUẤT KINH DOANH VÀ ĐÓNG GÓI BÁO CÁO KHOA HỌC

### 1. QUY TẮC BẮT BUỘC KHI THỰC THI CHO AGENT (AGY)

1. **Tự động hóa hoàn toàn:** Agent (`agy`) đọc tài liệu này, tự khởi tạo các module mã nguồn Python tương ứng, tự thực thi trong môi trường cục bộ và tự động kiểm tra tính hợp lệ của toàn bộ các sản phẩm đầu ra (`.csv`, `.py`, `.docx`, `.md`). Tuyệt đối không yêu cầu người dùng thao tác thủ công.
2. **Quy tắc bảo mật & danh tính:** Không đưa tên riêng, thông tin cá nhân hay bất kỳ định danh nào vào mã nguồn, chú thích (comment), file cấu hình hay báo cáo. Cố định `random_state = 42`.
3. **Trung thực số liệu (Zero-Fabrication):** Mọi số liệu trong các bảng Star-Schema, bảng ma trận hành động kinh doanh và báo cáo Word bắt buộc phải được đọc và trích xuất trực tiếp từ các file kết quả thực nghiệm đã sinh ra từ Giai đoạn 1 đến 4. Nghiêm cấm gán cứng giá trị giả định.
4. **Trọng tâm Insight và Giá trị kinh doanh:** Toàn bộ phát hiện từ mô hình (GMM, Survival, Uplift, SHAP, Expected Profit) phải được chuyển hóa thành các đề xuất kinh doanh cụ thể, có phân định rõ: Mục tiêu, Đối tượng nhắm chọn, Kênh can thiệp, Ngưỡng hành động, Rủi ro đi kèm và KPI đo lường định lượng.
5. **Quản trị tài nguyên phần cứng (Ryzen 5 3500U, 16GB RAM):**
   - Thiết lập `threads = 6`, `max_memory = '10GB'` khi xuất file dữ liệu lớn qua DuckDB.
   - Giải phóng RAM bằng `import gc; gc.collect()` sau khi hoàn tất các tác vụ xuất dữ liệu và tạo báo cáo.

---

### 2. CÁC TÁC VỤ LẬP TRÌNH VÀ THỰC THI CHI TIẾT

#### Tác vụ 5.1: Module xuất dữ liệu Star-Schema cho Power BI (`src/data_engineering/export_powerbi_star_schema.py`)

`agy` có nhiệm vụ tạo file `src/data_engineering/export_powerbi_star_schema.py` và chạy script để kết xuất 4 bảng CSV sạch vào thư mục `outputs/powerbi/`:

1. **Bảng Fact trung tâm: `fact_customer_decisions.csv` (200.000 dòng):**
   - Khóa liên kết: `customer_id`.
   - Kết hợp kết quả từ Feature Store PIT, dự đoán từ model tốt nhất (`outputs/models/best_calibrated_model.pkl`), phân khúc GMM và điểm số Uplift:
     - `target_actual`: Nhãn thực tế ($1$: Mua hàng, $0$: Không mua, `NULL` đối với 40.000 khách hàng tập Test).
     - `predicted_prob_calibrated`: Xác suất chuyển đổi sau hiệu chỉnh Isotonic/Platt.
     - `decision_optimal_tau`: Quyết định can thiệp tại ngưỡng tối ưu $\tau^*$ ($1$ nếu $p \ge \tau^*$, $0$ nếu $p < \tau^*$).
     - `uplift_score`: Điểm số tác động gia tăng $\tau_i = \mu_1(X_i) - \mu_0(X_i)$.
     - `uplift_segment`: Nhãn phân loại 4 nhóm (`Persuadables`, `Sure Things`, `Lost Causes`, `Sleeping Dogs`).
     - `gmm_cluster_id`: Mã cụm phân khúc hành vi RFM-E ($1$ đến $5$).
     - `clv_predicted_usd`: Giá trị đơn hàng trung bình dự kiến của khách hàng.
     - `expected_margin_usd`: Biên lợi nhuận gộp dự kiến: $25\% \times \text{AOV}_i$.
     - `expected_net_profit_usd`: Lợi nhuận ròng dự kiến: $\mathbb{I}(p_i \ge \tau^*) \cdot \left( y_i \cdot (\text{Margin}_i - C_{\text{voucher}}) - C_{\text{contact}} \right)$.
     - `decile_rank`: Thứ hạng phân vị từ $1$ (Top 10% xác suất cao nhất) đến $10$ (10% thấp nhất).
2. **Bảng Chiều khách hàng: `dim_customers.csv` (200.000 dòng):**
   - Khóa: `customer_id`.
   - Thuộc tính nhân khẩu học & hội viên: `age`, `age_group` (`<25`, `25-34`, `35-44`, `45-54`, `55+`), `gender`, `country`, `registration_date`, `customer_tier`, `loyalty_score`, `credit_limit`.
3. **Bảng Chiều hành vi giỏ hàng: `dim_cart_behavior.csv` (200.000 dòng):**
   - Khóa: `customer_id`.
   - Thuộc tính rào cản và tương tác: `total_cart_additions`, `cart_to_page_ratio`, `cart_abandonment_severity`, `cart_velocity`, `hesitation_index`, `days_since_last_session`, `bounce_rate`, `abandonment_risk_level` (`Low`, `Medium`, `High`, `Severe`).
4. **Bảng Chiều mô phỏng ngưỡng tài chính: `dim_threshold_simulation.csv` (100 dòng):**
   - Đọc trực tiếp từ `outputs/tables/tbl_ch5_threshold_optimization_results.csv`.
   - Thuộc tính mô phỏng $\tau \in [0.01, 0.99]$: `threshold`, `total_contacts`, `true_positives`, `false_positives`, `expected_net_profit_usd`, `precision`, `recall`, `f1_score`, `roi_percentage`.

---

#### Tác vụ 5.2: Xây dựng Ứng dụng Web tương tác Streamlit (`app/app.py`)

`agy` có nhiệm vụ tạo file `app/app.py` kết nối trực tiếp với mô hình đã huấn luyện trong `outputs/models/best_calibrated_model.pkl` (tuyệt đối không dùng công thức giả lập).
Giao diện ứng dụng gồm 3 Tab chức năng chuyên nghiệp:

1. **Tab 1: Chẩn đoán rào cản giỏ hàng cá thể hóa (Customer Diagnostic & XAI):**
   - Cho phép nhập các tham số phiên của một khách hàng: `total_pages_viewed`, `total_cart_additions`, `session_duration_sec`, `days_since_last_session`, `shipping_method`, `customer_tier`, `loyalty_score`.
   - Nạp pipeline tiền xử lý và mô hình đã hiệu chỉnh để tính toán:
     - Xác suất mua hàng thực tế ($p$).
     - Cụm phân khúc hành vi GMM tương ứng.
     - Nhóm phân loại Uplift.
   - Hiển thị khuyến nghị can thiệp tự động: Cảnh báo rào cản nếu `hesitation_index` cao hoặc cước vận chuyển thuộc nhóm `Overnight`.
2. **Tab 2: Trình mô phỏng lợi nhuận chiến dịch What-If (Interactive Profit Simulator):**
   - Bố trí các thanh trượt tham số kinh tế:
     - Biên lợi nhuận gộp (% Margin): Mặc định $25\%$, dải điều chỉnh $[10\%, 50\%]$.
     - Chi phí tiếp cận marketing ($C_{\text{contact}}$): Mặc định $\$1.0$, dải điều chỉnh $[\$0.2, \$5.0]$.
     - Chi phí voucher kích hoạt ($C_{\text{voucher}}$): Mặc định $\$5.0$, dải điều chỉnh $[\$1.0, \$20.0]$.
   - Tính toán lại đường cong Expected Profit Curve và hiển thị điểm tối ưu $\tau^*$ dịch chuyển theo thời gian thực cùng mức lợi nhuận ròng tối đa đạt được.
3. **Tab 3: Bản đồ phân bổ can thiệp tiếp thị (Uplift & Strategy Matrix):**
   - Trực quan hóa tỷ trọng 4 nhóm khách hàng (_Persuadables_, _Sure Things_, _Lost Causes_, _Sleeping Dogs_).
   - Cung cấp nút bấm tải xuống danh sách mã khách hàng thuộc nhóm _Persuadables_ để gửi thẳng cho bộ phận thực thi chiến dịch Marketing Automation.

---

#### Tác vụ 5.3: Module tổng hợp Insight và Đề xuất chiến lược kinh doanh (`src/business_value/generate_business_recommendations.py`)

`agy` có nhiệm vụ tạo file `src/business_value/generate_business_recommendations.py` và chạy script để kết xuất ma trận chiến lược kinh doanh:

1. **Tổng hợp 4 Insight cốt lõi từ thực nghiệm:**
   - _Insight 1 (Điểm gãy rào cản cước vận chuyển):_ Dựa trên kết quả CoxPH và SHAP, chỉ ra việc lựa chọn phương thức giao hàng qua đêm (`Overnight`) làm tăng nguy cơ từ bỏ giỏ hàng lên bao nhiêu lần (Hazard Ratio $> 1$) ở nhóm khách hàng hạng Bronze/Silver.
   - _Insight 2 (Thời điểm vàng can thiệp giỏ hàng):_ Dựa trên đường cong Kaplan-Meier, chỉ ra mốc thời gian bán rã xác suất chuyển đổi (sau mốc $t^*$, xác suất mua lại giảm sâu dưới 15%).
   - _Insight 3 (Chống lãng phí ngân sách tiếp thị nhờ Uplift):_ Nhóm _Sure Things_ chiếm bao nhiêu % dân số; việc cắt giảm voucher cho nhóm này giúp tiết kiệm bao nhiêu chi phí mà không làm giảm doanh thu.
   - _Insight 4 (Lợi ích tối ưu hóa ngưỡng quyết định $\tau^_$):* So sánh việc áp dụng ngưỡng tối ưu $\tau^*$ so với ngưỡng mặc định $0.50$ giúp gia tăng bao nhiêu % lợi nhuận ròng và cải thiện tỷ suất hoàn vốn (ROI).
2. **Đề xuất 4 gói hành động kinh doanh cụ thể (Actionable Business Recommendations):**
   - _Gói hành động 1 (Giải tỏa rào cản chi phí vận chuyển - Shipping Friction Reduction):_
     - Đối tượng: Cụm _Cart Hesitators_ có tỷ lệ chọn `Overnight` cao nhưng bỏ giỏ.
     - Can thiệp: Thiết lập ngưỡng Free Shipping linh hoạt (Dynamic Threshold) khi giá trị giỏ hàng đạt 80% AOV.
     - KPI đo lường: Giảm 20% tỷ lệ `cart_abandonment_severity`.
   - _Gói hành động 2 (Can thiệp tiếp thị cá thể hóa dựa trên Uplift):_
     - Đối tượng: Duy nhất nhóm _Persuadables_.
     - Can thiệp: Cấp voucher giảm giá $\$5.0$ có giới hạn thời gian (Scarcity countdown). Tuyệt đối không gửi cho _Sure Things_ và _Sleeping Dogs_.
     - KPI đo lường: Tăng 25% tỷ lệ chuyển đổi thuần (Net Uplift Conversion).
   - _Gói hành động 3 (Chiến dịch kích hoạt tự động theo thời gian vàng):_
     - Đối tượng: Khách hàng có phiên thêm giỏ nhưng chưa thanh toán.
     - Can thiệp: Kích hoạt email/push notification tự động vào đúng giờ thứ 3 (trước khi bước vào vùng suy giảm của Kaplan-Meier), không chờ sau 48 giờ.
     - KPI đo lường: Tỷ lệ mở email $\ge 35\%$, tỷ lệ hoàn tất giỏ phục hồi $\ge 12\%$.
   - _Gói hành động 4 (Phân bổ ngân sách tiếp thị theo phân vị Decile Lift@K):_
     - Đối tượng: Tập trung 80% ngân sách tiếp cận vào Decile 1 và Decile 2 (Top 20% xác suất cao nhất).
     - Can thiệp: Chuyển đổi từ tiếp thị đại trà sang tiếp thị trọng điểm dựa trên xếp hạng Lift@K.
     - KPI đo lường: Giảm 60% chi phí tiếp cận khách hàng (CAC) trong khi vẫn thâu tóm trên 70% tổng lượng đơn hàng tiềm năng.
3. **Lưu trữ ma trận đề xuất:**
   - Xuất bảng ra file: `outputs/tables/tbl_ch5_business_action_matrix.csv` gồm các trường:
     `strategy_id`, `strategy_name`, `target_segment`, `behavioral_barrier_addressed`, `intervention_action`, `channel`, `optimal_threshold`, `potential_risks`, `mitigation_plan`, `target_kpi`.

---

#### Tác vụ 5.4: Module sinh tự động Báo cáo Word 6 phần, Slide thuyết trình và Kịch bản video (`src/utils/generate_deliverables.py`)

`agy` có nhiệm vụ tạo file `src/utils/generate_deliverables.py` và chạy script để kết xuất toàn bộ hồ sơ nghiệm thu dự án:

1. **Khởi tạo Báo cáo nghiên cứu học thuật (`docs/BaoCao_CuoiKy_ChiTiet.docx`):**
   - Sử dụng thư viện `python-docx` để sinh tài liệu có cấu trúc 6 phần học thuật chuẩn, dung lượng mục tiêu 70–85 trang (dưới 100 trang), font chữ Times New Roman/Arial, giãn dòng 1.3, không viết văn sáo rỗng, tập trung hoàn toàn vào cấu trúc luận cứ và bằng chứng định lượng:
     - **Phần 1: Giới thiệu nghiên cứu (10–12 trang):** Bối cảnh thương mại điện tử, rào cản giỏ hàng, tuyên ngôn bài toán kinh tế, phạm vi dữ liệu đa bảng, quy tắc Point-in-Time và đóng góp khoa học.
     - **Phần 2: Câu hỏi và Phương pháp nghiên cứu (12–14 trang):** 5 câu hỏi nghiên cứu, 4 giả thuyết kiểm định, thiết kế thực nghiệm kiểm soát rò rỉ, cơ sở lý thuyết của GMM, CatBoost/LightGBM/XGBoost, Kaplan-Meier, CoxPH, T-Learner Uplift, TreeSHAP và Expected Profit Optimization.
     - **Phần 3: Xử lý dữ liệu và Phân tích khám phá (EDA) (12–15 trang):** Kết quả Data Healing (bảng `tbl_ch1_data_healing_audit.csv`), từ điển đặc trưng (`tbl_ch3_feature_dictionary.csv`), kết quả kiểm định thống kê H1, H2, H3 (`tbl_ch3_hypothesis_test_results.csv`), phân tích phân phối nhãn và rào cản giỏ hàng.
     - **Phần 4: Xây dựng, Huấn luyện và Đánh giá mô hình Machine Learning (16–20 trang):** Kết quả Baseline (`tbl_ch4_model_benchmark_comparison.csv`), siêu tham số Optuna (`tbl_ch4_optuna_best_hyperparameters.csv`), đường cong Reliability Diagram, kết quả sống còn CoxPH (`tbl_ch4_coxph_hazard_ratios.csv`), ma trận 4 nhóm Uplift (`tbl_ch4_uplift_segments_summary.csv`), phân tích tương tác phi tuyến SHAP (`tbl_ch4_shap_top_interactions.csv`), Ablation Study và độ ổn định đa hạt giống (`tbl_ch4_multiseed_stability.csv`).
     - **Phần 5: Thiết kế Dashboard Power BI, Ứng dụng Web và Hàm ý kinh doanh (12–14 trang):** Cấu trúc Star-Schema 4 bảng, hướng dẫn DAX, kiến trúc Web Streamlit 3 tabs, đường cong tối ưu hóa lợi nhuận $\tau^*$ (`tbl_ch5_threshold_optimization_results.csv`), bảng 10 phân vị Decile Lift@K (`tbl_ch5_decile_lift_profit.csv`), 4 insight cốt lõi và ma trận đề xuất hành động kinh doanh (`tbl_ch5_business_action_matrix.csv`).
     - **Phần 6: Hạn chế, Hướng phát triển và Kết luận (6–8 trang):** Mức độ hoàn thành mục tiêu, các rào cản dữ liệu thực tế, định hướng thử nghiệm A/B Testing ngoài mẫu và Danh mục toàn diện 26 Tài liệu tham khảo chuẩn APA 7th (2021–2026).
   - Tự động đọc và chèn bảng số liệu định dạng chuẩn (Header đậm, căn lề số) từ các file `.csv` trong `outputs/tables/`.
   - Tại mọi vị trí biểu đồ, tự động chèn khối trích dẫn thống nhất:
     > **[VỊ TRÍ CHÈN ẢNH BÁO CÁO]**  
     > **Thư mục & Tệp:** `outputs/figures/<tên_file>.png`  
     > **Tiêu đề hình:** _Hình X.Y. <Tên tiêu đề phản ánh insight>._  
     > **Nguồn trích xuất:** Thực nghiệm từ pipeline `<tên_script>.py`.  
     > **Ý nghĩa kinh tế:** _<Đoạn văn 2-3 câu diễn giải số liệu và chỉ ra điểm mấu chốt>._

2. **Khởi tạo Dàn ý Slide thuyết trình (`docs/SLIDE_OUTLINE.md`):**
   - Cấu trúc 18 slide tinh gọn, tập trung 80% thời lượng vào Insight rào cản giỏ hàng và Bằng chứng tối ưu hóa lợi nhuận kinh tế (không kể lể quy trình kỹ thuật sơ đẳng).

3. **Khởi tạo Kịch bản Video Demo (`docs/VIDEO_SCRIPT.md`):**
   - Kịch bản chi tiết từng mốc thời gian (tổng thời lượng 3–5 phút):
     - 00:00 - 00:45: Giới thiệu vấn đề rào cản giỏ hàng và mục tiêu tối ưu lợi nhuận.
     - 00:45 - 01:45: Trực quan hóa phát hiện rào cản giỏ hàng và phân khúc GMM/Survival.
     - 01:45 - 03:00: Demo tương tác ứng dụng Streamlit (chuẩn đoán cá thể hóa, What-If simulator tìm $\tau^*$, Uplift matrix).
     - 03:00 - 04:00: Kết luận giá trị kinh tế mang lại (Tăng lợi nhuận ròng, giảm CAC qua Lift@K).

4. **Khởi tạo Kịch bản thực thi tự động toàn diện (`run_pipeline.py`):**
   - Viết file script `run_pipeline.py` tại thư mục gốc điều phối toàn bộ các script từ Giai đoạn 1 đến Giai đoạn 5 theo thứ tự tuần tự, tự động ghi log vào `outputs/experiments/pipeline_run.log`.

---

### 3. QUY TRÌNH THỰC THI TỰ ĐỘNG CHO AGENT

Khi kích hoạt giai đoạn 5, `agy` tự động chạy tuần tự các lệnh sau trong terminal, tự kiểm tra mã lỗi và hoàn tất toàn bộ pipeline:

```bash
python src/data_engineering/export_powerbi_star_schema.py
python src/business_value/generate_business_recommendations.py
python src/utils/generate_deliverables.py
```

---

### 4. TIÊU CHÍ NGHIỆM THU HOÀN THÀNH (DEFINITION OF DONE)

Giai đoạn 5 được coi là hoàn tất khi:

- [ ] Thư mục `outputs/powerbi/` chứa đầy đủ 4 file CSV chuẩn Star Schema: `fact_customer_decisions.csv` (200.000 dòng), `dim_customers.csv`, `dim_cart_behavior.csv`, `dim_threshold_simulation.csv`.
- [ ] Tệp `outputs/tables/tbl_ch5_business_action_matrix.csv` được tạo đầy đủ 4 gói chiến lược kinh doanh định lượng.
- [ ] Ứng dụng `app/app.py` chạy thành công bằng lệnh `streamlit run app/app.py`, nạp model thực tế không phát sinh lỗi.
- [ ] Tệp báo cáo Word `docs/BaoCao_CuoiKy_ChiTiet.docx` được sinh ra hoàn chỉnh với cấu trúc 6 phần, độ dài từ 70 đến 85 trang, tự động chèn đầy đủ các bảng dữ liệu thực nghiệm và khối trích dẫn hình ảnh.
- [ ] Hai tệp tài liệu `docs/SLIDE_OUTLINE.md` (18 slide) và `docs/VIDEO_SCRIPT.md` (kịch bản 3–5 phút) được tạo đầy đủ nội dung chuyên sâu.
- [ ] File điều phối `run_pipeline.py` tại thư mục gốc thực thi thành công từ đầu đến cuối chỉ với một lệnh duy nhất.

```

```
