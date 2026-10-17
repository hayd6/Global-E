# BẢN ĐẶC TẢ YÊU CẦU DỰ ÁN (PROJECT REQUIREMENTS DOCUMENT - PRD)

## 1. TỔNG QUAN DỰ ÁN

- **Tên đề tài:** Phân tích rào cản chuyển đổi giỏ hàng và tối ưu hóa lợi nhuận tiếp thị trong thương mại điện tử.
- **Mục tiêu học thuật & ứng dụng:** Chuyển hóa toàn diện bài toán từ phân tích mô tả tĩnh sang khung phân tích hỗ trợ ra quyết định kinh tế (Prescriptive Decision Framework). Dự án giải quyết các vấn đề:
  1. Nhận diện các điểm gãy và rào cản hành vi trong phễu giỏ hàng (Cart Abandonment Friction Points).
  2. Phân khúc khách hàng động theo xác suất thành viên hỗn hợp (GMM) và mật độ (HDBSCAN).
  3. Dự đoán xác suất mua hàng trong 30 ngày bằng các mô hình tăng cường độ dốc (CatBoost, LightGBM, XGBoost) tối ưu qua Optuna, đi kèm hiệu chỉnh xác suất thực nghiệm (Probability Calibration).
  4. Định lượng thời gian phân rã cơ hội của giỏ hàng (Cart Survival Analysis) và tỷ số nguy cơ rời bỏ (CoxPH Hazard Ratios).
  5. Đánh giá tác động can thiệp tiếp thị qua mô hình hóa nâng nhấc (Uplift Modeling / CATE) nhằm loại bỏ lãng phí ngân sách ưu đãi.
  6. Tối đa hóa hàm lợi nhuận kinh tế kỳ vọng (Expected Profit Optimization) để tìm ngưỡng quyết định $\tau^*$ thay thế ngưỡng 0.5 mặc định.
- **Tiêu chuẩn dữ liệu:** Tuân thủ nghiêm ngặt nguyên tắc Point-in-Time (PIT), loại bỏ hoàn toàn rò rỉ dữ liệu (Data Leakage) theo thời gian và phân vùng dữ liệu độc lập.

---

## 2. HẠ TẦNG KỸ THUẬT & TÀI NGUYÊN THỰC THI

- **Môi trường:** Python 3.10+, VS Code / Antigravity IDE.
- **Cấu hình phần cứng đích:** CPU AMD Ryzen 5 3500U (4 cores / 8 threads), 16GB RAM.
- **Ràng buộc tài nguyên mã nguồn:**
  - Giới hạn DuckDB: `SET threads = 6; SET max_memory = '10GB';`.
  - Xử lý dữ liệu lớn: Tận dụng cơ chế In-Process OLAP dạng cột của DuckDB, xuất dữ liệu trung gian dạng Apache Parquet (`snappy` compression), giải phóng bộ nhớ tường minh qua `gc.collect()`.
  - Huấn luyện mô hình: `n_jobs = 6` hoặc `thread_count = 6`.

---

## 3. CẤU TRÚC DỮ LIỆU ĐẦU VÀO (`data/raw/`)

Dự án sử dụng 8 bảng dữ liệu gốc:

1. `customers.csv` (200.000 dòng): `customer_id`, `age`, `gender`, `country`, `registration_date`, `customer_tier`, `loyalty_score`, `credit_limit`, `email_open_rate`, `discount_usage_rate`, `referral_code`, `review_score`.
2. `sessions.csv` (2.000.000 dòng): `session_id`, `customer_id`, `session_start_time`, `session_duration_sec`, `pages_viewed`, `cart_additions`, `bounce_flag`, `traffic_source`, `device_category`, `campaign_id`, `geo_ip_region`.
3. `transactions.csv` (500.000 dòng): `transaction_id`, `customer_id`, `transaction_timestamp`, `order_value`, `items_count`, `payment_method`, `discount_applied`, `shipping_method`, `high_value_flag`.
4. `marketing_campaigns.csv` (200 dòng): `campaign_id`, `campaign_name`, `channel`, `start_date`, `end_date`, `budget`.
5. `geo_data.csv` (100 dòng): `geo_ip_region`, `region_name`, `average_income`, `urban_ratio`, `internet_penetration`.
6. `train.csv` (160.000 dòng): `customer_id`, `target`.
7. `test.csv` (40.000 dòng): `customer_id`.
8. `sample_submission.csv` (40.000 dòng): Mẫu kết quả.

---

## 4. QUY TRÌNH KỸ THUẬT VÀ NGUYÊN TẮC BẢO TOÀN POINT-IN-TIME (PIT)

### 4.1. Kiểm toán & Khắc phục sai lệch dữ liệu gốc (Data Healing)

- **Phiên và giao dịch trước ngày đăng ký:** Loại bỏ hoặc điều chỉnh các bản ghi sự kiện có mốc thời gian nhỏ hơn `registration_date`.
- **Giao dịch bất thường:** Lọc bỏ các dòng có `items_count <= 0` nhưng `order_value > 0`.
- **Chuẩn hóa giá trị:** Ép kiểu `order_value` thành số thực; chuẩn hóa các trường nhị phân (`bounce_flag`, `discount_applied`) thành $\{0, 1\}$.
- **Xử lý missing value:** Điền trung vị cho biến số, tạo nhãn `Unknown` cho biến phân loại trên tập Train, chỉ dùng tham số đã học để transform tập Holdout.

### 4.2. Ranh giới thời gian PIT ($t_0$)

- Mốc chốt $t_0$ được ấn định sao cho:
  - Toàn bộ đặc trưng lịch sử $X$ chỉ tính từ dữ liệu phát sinh tại thời điểm $\le t_0$.
  - Nhãn $y_i \in \{0, 1\}$ được xác định dựa trên việc khách hàng $i$ có phát sinh giao dịch trong cửa sổ tương lai $(t_0, t_0 + 30\text{ ngày}]$ hay không.

### 4.3. Tập đặc trưng hành vi bậc cao (Advanced Behavioral Feature Store)

Trích xuất tối thiểu 45 đặc trưng cấp khách hàng, tập trung vào rào cản giỏ hàng:

- **Nhóm tương tác & rào cản giỏ hàng:**
  - `total_cart_additions`: Tổng số lượt thêm giỏ.
  - `cart_to_page_ratio`: $\frac{\text{total\_cart\_additions}}{\text{total\_pages\_viewed} + 1}$.
  - `cart_abandonment_severity`: Số phiên có thêm giỏ nhưng không giao dịch.
  - `cart_velocity`: Số lượt thêm giỏ trên mỗi phiên hoạt động.
  - `abandonment_rate_historical`: Tỷ lệ các phiên bỏ quên giỏ hàng.
- **Nhóm thời gian & phân rã tương tác:**
  - `recency_days`: Số ngày từ phiên cuối cùng đến $t_0$.
  - `inter_session_time_mean`: Khoảng cách trung bình giữa các phiên liên tiếp.
  - `activity_trend_slope`: Độ dốc tương tác (tăng hay giảm số phiên trong 30 ngày gần $t_0$ so với 30 ngày trước đó).
- **Nhóm giá trị & nhạy cảm ưu đãi:**
  - `avg_order_value`: Giá trị đơn trung bình.
  - `discount_elasticity`: Tỷ lệ giao dịch dùng mã giảm giá trên tổng số giao dịch.
  - `shipping_friction_ratio`: Tỷ lệ đơn hàng sử dụng giao hàng hỏa tốc/qua đêm (chi phí cao).

---

## 5. CẤU TRÚC 6 TRỤ CỘT MÔ HÌNH HÓA VÀ THUẬT TOÁN

### Trụ cột 1: Phân khúc hành vi & Khám phá rào cản

- **Thuật toán:**
  - _K-Means (Baseline):_ Đánh giá qua Elbow curve và Silhouette score.
  - _Gaussian Mixture Models (GMM - Nâng cao):_ Ước lượng xác suất phân cụm mềm (Soft Clustering), chọn số cụm bằng Bayesian Information Criterion (BIC) và Akaike Information Criterion (AIC).
  - _HDBSCAN (Nâng cao):_ Phân cụm dựa trên mật độ và lọc bỏ nhiễu/ngoại lai (outliers/noise).
- **Kiểm định giả thuyết hành vi:**
  - Sử dụng kiểm định Kruskal-Wallis cho từng đặc trưng giỏ hàng giữa các cụm.
  - Phân tích hậu kiểm (Post-hoc) Mann-Whitney U test đi kèm hiệu chỉnh Bonferroni ($p < 0.05$).

### Trụ cột 2: Dự đoán chuyển đổi (Propensity Modeling) & Tối ưu siêu tham số

- **Thuật toán so sánh:**
  - Baseline: Logistic Regression, Random Forest.
  - SOTA Boosting: CatBoost, LightGBM, XGBoost.
  - Stacking Ensemble: Kết hợp Out-of-Fold predictions của CatBoost + LightGBM + Random Forest qua Logistic Regression Meta-Learner.
- **Tối ưu hóa siêu tham số:**
  - Khung Optuna (Tree-structured Parzen Estimator - TPE) với 35 trials cho mỗi thuật toán boosting.
  - Tích hợp `EarlyStoppingCallback` (dừng sau 7 trials không cải thiện).
  - Hàm mục tiêu tối ưu: PR-AUC trên 5-Fold Stratified Cross-Validation.

### Trụ cột 3: Hiệu chỉnh xác suất (Probability Calibration)

- **Kỹ thuật:** So sánh Isotonic Regression và Platt Scaling (Sigmoid).
- **Đo lường:** Brier Score và Expected Calibration Error (ECE) trước và sau hiệu chỉnh. Đảm bảo xác suất $p_i \in [0, 1]$ phản ánh đúng tần suất thực tế để làm đầu vào cho hàm lợi nhuận.

### Trụ cột 4: Mô hình hóa sống còn của giỏ hàng (Survival Analysis)

- **Kaplan-Meier Estimator:** Ước lượng hàm sống còn $S(t) = P(T > t)$ biểu thị xác suất khách hàng chưa từ bỏ hoàn toàn giỏ hàng sau thời gian $t$ kể từ phiên tương tác cuối.
- **Cox Proportional Hazards Model:**
  $$h(t \mid X) = h_0(t) \exp\left(\sum_{j=1}^p \beta_j X_j\right)$$
  Tính toán Tỷ số nguy cơ (Hazard Ratios: $\text{HR}_j = \exp(\beta_j)$) của các yếu tố rào cản (chi phí vận chuyển, không có voucher, thời lượng phiên ngắn).

### Trụ cột 5: Suy luận nhân quả & Tối ưu can thiệp tiếp thị (Uplift Modeling)

- **Mô hình:** Meta-Learner (T-Learner sử dụng 2 mô hình LightGBM riêng biệt cho nhóm Treatment $W=1$ và nhóm Control $W=0$).
- **Ước lượng CATE:**
  $$\tau_i = \mathbb{E}[Y_i(1) - Y_i(0) \mid X_i]$$
- **Phân loại 4 nhóm phản ứng:**
  1. _Persuadables:_ $\tau_i > 0$ và có ý nghĩa thống kê (Can thiệp tiếp thị tối đa).
  2. _Sure Things:_ $Y_i(0) = 1$ (Khách hàng tự mua, cấm gửi voucher để bảo toàn biên lợi nhuận).
  3. _Lost Causes:_ $Y_i(1) = 0$ và $Y_i(0) = 0$ (Không can thiệp, tránh lãng phí chi phí tiếp cận).
  4. _Sleeping Dogs:_ $\tau_i < 0$ (Can thiệp gây khó chịu, tuyệt đối tránh).

### Trụ cột 6: Giải thích tương tác SHAP & Tối ưu hóa lợi nhuận kỳ vọng

- **TreeSHAP Interaction Analysis:** Tính toán giá trị tương tác cặp đặc trưng $\Phi_{i,j}$ để chỉ ra các hiệu ứng phi tuyến tính giữa rào cản giỏ hàng và các thuộc tính khác.
- **Khung tối ưu hóa lợi nhuận kỳ vọng (Expected Profit Curve):**
  - Thiết lập phương trình kinh tế:
    $$\text{Profit}(\tau) = \sum_{i \in \text{Holdout}} \left[ \mathbb{I}(p_i \ge \tau) \cdot \left( y_i \cdot (\text{Margin}_i - C_{\text{voucher}}) - C_{\text{contact}} \right) \right]$$
  - Tham số chuẩn hóa: Biên lợi nhuận gộp $= 25\% \times \text{order\_value}$; $C_{\text{contact}} = \$1.0$; $C_{\text{voucher}} = \$5.0$.
  - Quét ngưỡng xác suất $\tau \in [0.01, 0.99]$ với bước nhảy $0.01$ để tìm ngưỡng cực đại hóa lợi nhuận $\tau^*$.
- **Phân vị Decile & Lift@K:** Lập bảng 10 phân vị (Deciles 1–10) tính toán Precision@K, Recall@K, Lift@K và Cumulative Gain.

---

## 6. QUẢN TRỊ THỰC NGHIỆM VÀ KIỂM THỬ TỰ ĐỘNG

- **Phân chia dữ liệu:** Tách `train.csv` thành Train Pool (80% = 128.000 dòng) và Holdout Test (20% = 32.000 dòng) theo phân tầng nhãn `target`.
- **Cơ chế chống rò rỉ:**
  - Toàn bộ pipeline `fit()` trên Train Pool, chỉ `transform()` trên Holdout Test.
  - Tách kiểm tra tính độc lập tập hợp: $\text{Set}(\text{ID}_{\text{Train}}) \cap \text{Set}(\text{ID}_{\text{Holdout}}) = \emptyset$.
- **Kiểm định đa hạt giống (Multi-Seed Testing):** Chạy kiểm chứng trên 5 hạt giống: `[42, 100, 2024, 2026, 777]`, báo cáo Mean $\pm$ Standard Deviation.
- **Ablation Study:** So sánh hiệu năng mô hình khi loại bỏ tuần tự từng nhóm đặc trưng:
  1. Full Features.
  2. No Cart Engagement Features.
  3. No Historical Transaction Features.
  4. No Demographic Features.

---

## 7. TIÊU CHUẨN ĐỒ HỌA VÀ ĐẦU RA BÀN GIAO

- **Quy chuẩn đồ họa (300 DPI, Tri-Color):**
  - Nền: `#F8FAFC`.
  - Màu chủ đạo: `#0F172A` (Midnight Navy).
  - Màu nhấn tích cực: `#0D9488` (Forest Emerald).
  - Màu nhấn cảnh báo: `#E11D48` (Crimson Coral).
  - Font: Sans-serif, bỏ viền trên/phải (`despine`), kẻ lưới phụ `alpha = 0.3`, trực quan hóa nhãn trực tiếp (Direct Callouts).
- **Đầu ra Power BI (`outputs/powerbi/`):**
  - `fact_customer_decisions.csv` (200.000 dòng đầy đủ).
  - `dim_customers.csv`.
  - `dim_cart_behavior.csv`.
  - `dim_threshold_simulation.csv` (mô phỏng 100 ngưỡng).
- **Báo cáo nghiên cứu khoa học:** Cấu trúc 6 phần, dung lượng 70–85 trang, tuyệt đối không nhập số liệu thủ công, 100% số liệu truy xuất từ `outputs/tables/` và `outputs/figures/`.
