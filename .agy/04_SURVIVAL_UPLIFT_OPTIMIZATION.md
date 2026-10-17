# .agy/04_SURVIVAL_UPLIFT_OPTIMIZATION.md

## GIAI ĐOẠN 4: MÔ HÌNH HÓA SỐNG CÒN GIỎ HÀNG, UPLIFT MODELING, SHAP INTERACTION VÀ TỐI ƯU HÓA LỢI NHUẬN KINH TẾ

### 1. QUY TẮC BẮT BUỘC KHI THỰC THI CHO AGENT (AGY)

1. **Tự động hóa hoàn toàn:** Agent (`agy`) đọc tài liệu này, tự khởi tạo các module mã nguồn Python tương ứng, tự thực thi trong môi trường cục bộ và tự động kiểm tra tính hợp lệ của các file kết quả (`.csv`, `.json`, `.png`). Tuyệt đối không yêu cầu người dùng thao tác thủ công.
2. **Quy tắc bảo mật & danh tính:** Không đưa tên riêng, thông tin cá nhân hay bất kỳ định danh nào vào mã nguồn, chú thích (comment) hay tên tệp. Cố định `random_state = 42`.
3. **Trung thực số liệu (Zero-Fabrication):** Mọi chỉ số đánh giá (Hazard Ratio, CATE, Qini Score, SHAP Interaction Values, Expected Profit, Lift@K) bắt buộc phải tính toán trực tiếp từ dữ liệu thực nghiệm trên tập Holdout Test. Nghiêm cấm gán cứng giá trị giả định.
4. **Quản trị tài nguyên phần cứng (Ryzen 5 3500U, 16GB RAM):**
   - Thiết lập `n_jobs = 6` hoặc `thread_count = 6` cho các tác vụ phân tích và giải thích.
   - Khi tính toán SHAP Interaction Values (ma trận tương tác tốn kém tài nguyên), lấy mẫu đại diện phân tầng có kiểm soát $N = 2.000$ quan sát từ tập Holdout Test để tránh tràn RAM và quá tải CPU.
   - Giải phóng RAM bằng `import gc; gc.collect()` sau mỗi bước chạy thuật toán.

---

### 2. CÁC TÁC VỤ LẬP TRÌNH VÀ THỰC THI CHI TIẾT

#### Tác vụ 4.1: Module phân tích sống còn của giỏ hàng và nguy cơ rời bỏ (`src/analytics/survival_analysis.py`)

`agy` có nhiệm vụ tạo file `src/analytics/survival_analysis.py` và chạy script với các yêu cầu:

1. **Thiết lập biến phân tích sống còn (Time-to-Event Data):**
   - Đọc dữ liệu từ `data/processed/customer_features_pit.parquet` kết hợp bảng giao dịch gốc đã làm sạch.
   - Xác định trục thời gian $T$: Số ngày kể từ phiên truy cập có thêm giỏ hàng gần nhất đến thời điểm phát sinh giao dịch thành công (hoặc đến mốc chốt $t_0$ nếu không mua).
   - Xác định biến biến cố $E$: $E = 1$ nếu khách hàng chuyển đổi thành công trong cửa sổ quan sát; $E = 0$ nếu bị kiểm duyệt phải (Right-Censored - từ bỏ giỏ hàng).
2. **Ước lượng đường cong sống còn Kaplan-Meier:**
   - Sử dụng `lifelines.KaplanMeierFitter`.
   - Ước lượng hàm sống còn tổng thể $S(t) = P(T > t)$ biểu thị xác suất một giỏ hàng chưa bị từ bỏ hoàn toàn sau thời gian $t$.
   - Ước lượng đường cong phân tầng theo các yếu tố rào cản:
     - Theo phương thức vận chuyển: `Standard` vs `Express` vs `Overnight`.
     - Theo hành vi ưu đãi: Có áp dụng mã giảm giá (`discount_applied = 1`) vs Không áp dụng (`discount_applied = 0`).
     - Theo hạng thành viên: `customer_tier` (Bronze, Silver, Gold, Platinum).
   - Xác định "Thời điểm vàng can thiệp": Mốc thời gian $t^*$ mà tại đó xác suất sống còn của giỏ hàng giảm xuống dưới 15% (thời điểm giỏ hàng sắp bị từ bỏ vĩnh viễn).
3. **Mô hình hồi quy rủi ro tỷ lệ Cox (Cox Proportional Hazards Model):**
   - Sử dụng `lifelines.CoxPHFitter(penalizer=0.01)`.
   - Đưa vào các biến đồng biến (Covariates): `cart_to_page_ratio`, `cart_abandonment_severity`, `pct_overnight_shipping`, `discount_usage_rate`, `bounce_rate`, `loyalty_score`.
   - Trích xuất bảng Tỷ số nguy cơ (Hazard Ratio: $\text{HR} = \exp(\beta)$) kèm khoảng tin cậy 95% và giá trị $p$-value.
   - Xuất kết quả ra file: `outputs/tables/tbl_ch4_coxph_hazard_ratios.csv`.
   - Xuất bảng tóm tắt thời gian bán rã giỏ hàng ra: `outputs/tables/tbl_ch4_survival_summary.csv`.

---

#### Tác vụ 4.2: Module suy luận nhân quả và mô hình hóa tác động tiếp thị (`src/models/uplift_modeling.py`)

`agy` có nhiệm vụ tạo file `src/models/uplift_modeling.py` và chạy script với các yêu cầu:

1. **Thiết lập bài toán Uplift / CATE:**
   - Biến can thiệp Treatment $W$: Khách hàng có tiếp xúc chiến dịch tiếp thị hoặc nhận ưu đãi ($W = 1$) so với đối chứng không can thiệp ($W = 0$).
   - Biến kết quả $Y$: Nhãn chuyển đổi mua hàng ($target \in \{0, 1\}$).
2. **Triển khai T-Learner (Two-Model Meta-Learner):**
   - Huấn luyện mô hình $\mu_1(X) = \mathbb{E}[Y \mid X, W=1]$ trên tập mẫu có can thiệp bằng `LGBMClassifier(random_state=42, n_jobs=6)`.
   - Huấn luyện mô hình $\mu_0(X) = \mathbb{E}[Y \mid X, W=0]$ trên tập mẫu đối chứng bằng `LGBMClassifier(random_state=42, n_jobs=6)`.
   - Ước lượng Uplift Score cá thể hóa trên tập Holdout Test:
     $$\tau_i = \mu_1(X_i) - \mu_0(X_i)$$
3. **Phân loại ma trận 4 nhóm phản ứng kinh doanh:**
   - Phân loại từng khách hàng dựa trên $\mu_1(X_i)$ và $\mu_0(X_i)$ theo ngưỡng phân vị:
     - _Persuadables:_ $\tau_i > 0$ ở mức cao (Nhóm nhạy cảm: Chỉ mua nếu có can thiệp/voucher $\rightarrow$ Ưu tiên số 1).
     - _Sure Things:_ $\mu_0(X_i)$ cao và $\tau_i \approx 0$ (Nhóm chắc chắn mua: Tự mua không cần ưu đãi $\rightarrow$ Cấm gửi voucher để bảo toàn biên lợi nhuận).
     - _Lost Causes:_ $\mu_1(X_i) \approx 0$ và $\mu_0(X_i) \approx 0$ (Nhóm bất khả thi: Tốn chi phí tiếp thị cũng không mua $\rightarrow$ Loại bỏ).
     - _Sleeping Dogs:_ $\tau_i < 0$ (Nhóm phản tác dụng: Can thiệp tiếp thị gây khó chịu làm giảm tỷ lệ mua $\rightarrow$ Tránh xa).
   - Xuất bảng phân bổ và tỷ lệ đóng góp ra: `outputs/tables/tbl_ch4_uplift_segments_summary.csv`.
4. **Đo lường năng lực phân bổ can thiệp (Qini Metric):**
   - Tính toán hệ số Qini Curve và diện tích dưới đường cong Qini (Qini Score) so sánh với đường phân bổ ngẫu nhiên.

---

#### Tác vụ 4.3: Module giải thích tương tác đặc trưng phi tuyến (`src/explainability/shap_interaction.py`)

`agy` có nhiệm vụ tạo file `src/explainability/shap_interaction.py` và chạy script với các yêu cầu:

1. **TreeSHAP trên mô hình tối ưu:**
   - Nạp mô hình hiệu chỉnh tốt nhất từ `outputs/models/best_calibrated_model.pkl`.
   - Trích xuất mẫu $N = 2.000$ quan sát phân tầng từ tập Holdout Test.
   - Khởi tạo `shap.TreeExplainer(model)`.
2. **Tính toán ma trận tương tác cặp đặc trưng (SHAP Interaction Values):**
   - Tính toán toàn bộ ma trận tương tác $\Phi_{i,j}$ với chiều $(N, p, p)$.
   - Tính toán độ mạnh tương tác trung bình toàn cục:
     $$I_{j,k} = \frac{1}{N} \sum_{i=1}^N \vert{}\Phi_{i, j, k}\vert{} \quad (j \ne k)$$
3. **Bóc tách các rào cản giỏ hàng phi tuyến:**
   - Lọc và xếp hạng 5 cặp tương tác mạnh nhất liên quan đến rào cản giỏ hàng:
     - Tương tác giữa `cart_to_page_ratio` và `discount_usage_rate`.
     - Tương tác giữa `days_since_last_session` và `pct_overnight_shipping`.
     - Tương tác giữa `cart_abandonment_severity` và `loyalty_score`.
   - Xuất bảng kết quả chi tiết ra: `outputs/tables/tbl_ch4_shap_top_interactions.csv` (gồm: `feature_1`, `feature_2`, `mean_absolute_interaction_value`, `behavioral_interpretation`).

---

#### Tác vụ 4.4: Module tối ưu hóa lợi nhuận kinh tế kỳ vọng và phân vị Decile Lift@K (`src/business_value/profit_optimization.py`)

`agy` có nhiệm vụ tạo file `src/business_value/profit_optimization.py` và chạy script với các yêu cầu:

1. **Định lượng hàm lợi nhuận kinh tế kỳ vọng (Expected Profit Optimization):**
   - Đọc các tham số giả định kinh tế từ `configs/base_config.yaml`:
     - Biên lợi nhuận gộp: $\text{Gross Margin Rate} = 25\%$ trên giá trị đơn hàng trung bình ($AOV$).
     - Chi phí tiếp cận marketing cơ bản: $C_{\text{contact}} = \$1.0$ / khách hàng.
     - Chi phí phát hành voucher kích hoạt: $C_{\text{voucher}} = \$5.0$ / khách hàng.
   - Trên tập Holdout Test (32.000 khách hàng), với mỗi khách hàng $i$, tính giá trị biên lợi nhuận kỳ vọng: $\text{Margin}_i = 0.25 \times \text{avg\_order\_value}_i$.
   - Quét dải ngưỡng xác suất $\tau \in [0.01, 0.99]$ với bước nhảy $0.01$:
     $$\text{Profit}(\tau) = \sum_{i \in \text{Holdout}} \left[ \mathbb{I}(p_i \ge \tau) \cdot \left( y_i \cdot (\text{Margin}_i - C_{\text{voucher}}) - C_{\text{contact}} \right) \right]$$
   - Xác định ngưỡng tối ưu $\tau^*$ đạt đỉnh lợi nhuận kinh tế. So sánh chi tiết lợi nhuận, ROI và số lượng khách hàng phải tiếp cận tại $\tau^*$ so với ngưỡng mặc định $\tau = 0.50$.
   - Xuất bảng mô phỏng ngưỡng ra: `outputs/tables/tbl_ch5_threshold_optimization_results.csv`.
2. **Lập bảng hiệu năng phân vị 10 Deciles và Lift@K:**
   - Xếp hạng 32.000 khách hàng tập Holdout theo xác suất dự đoán $p_i$ giảm dần.
   - Chia thành 10 Deciles bằng nhau (Decile 1 là Top 10% xác suất cao nhất, Decile 10 là 10% thấp nhất).
   - Với mỗi Decile $k \in [1, 10]$, tính toán:
     - Số lượng khách hàng ($N_k$).
     - Số lượng người mua thực tế ($Y_k$).
     - Tỷ lệ phản hồi (Response Rate: $\frac{Y_k}{N_k}$).
     - Tỷ lệ thâu tóm tích lũy (Cumulative Recall / Capture Rate).
     - Precision@K và Recall@K.
     - Lift@K: $\frac{\text{Response Rate of Decile } k}{\text{Overall Response Rate}}$.
     - Lợi nhuận ròng tích lũy (Cumulative Net Profit).
   - Xuất bảng ra file: `outputs/tables/tbl_ch5_decile_lift_profit.csv`.

---

#### Tác vụ 4.5: Module xuất biểu đồ phân tích chuyên sâu chuẩn xuất bản 300 DPI (`src/business_value/plot_business_insights.py`)

`agy` có nhiệm vụ tạo file `src/business_value/plot_business_insights.py` và chạy script để kết xuất hình ảnh:

- Quy chuẩn đồ họa bắt buộc: Nền `#F8FAFC`, Khối chính `#0F172A`, Nhấn tích cực `#0D9488`, Nhấn rào cản `#E11D48`, độ phân giải 300 DPI, font chữ sans-serif, despine viền trên/phải, lưới phụ mờ `alpha = 0.3`.
  Nội dung 4 biểu đồ cần xuất:

1. `outputs/figures/fig_ch4_04_survival_cart_decay.png`:
   - Biểu đồ đường cong sống còn Kaplan-Meier phân tầng theo phương thức vận chuyển (`Standard`, `Express`, `Overnight`).
   - Có đường nét đứt đỏ `#E11D48` và khung Callout chỉ rõ "Thời điểm vàng can thiệp": Sau mốc thời gian $t^*$, xác suất mua lại giảm sâu dưới 15%.
2. `outputs/figures/fig_ch4_05_uplift_qini_curve.png`:
   - Biểu đồ đường cong Qini Curve so sánh mô hình T-Learner với đường phân bổ ngẫu nhiên (Random Line), thể hiện số lượng đơn hàng gia tăng tích lũy.
3. `outputs/figures/fig_ch4_06_shap_interaction_matrix.png`:
   - Biểu đồ nhiệt (Heatmap) thể hiện ma trận tương tác SHAP giữa top các đặc trưng rào cản giỏ hàng và đặc trưng hành vi.
4. `outputs/figures/fig_ch5_01_expected_profit_optimization.png`:
   - Đồ thị đường cong Lợi nhuận kinh tế kỳ vọng (Expected Profit Curve) theo ngưỡng quyết định $\tau \in [0.01, 0.99]$.
   - Có đường gióng nét đứt màu xanh `#0D9488` tại ngưỡng tối ưu $\tau^*$ và đường gióng màu xám tại ngưỡng mặc định $\tau = 0.50$, kèm ghi chú chênh lệch lợi nhuận ròng đạt được ($+\Delta \text{ Profit}$).

---

### 3. QUY TRÌNH THỰC THI TỰ ĐỘNG CHO AGENT

Khi kích hoạt giai đoạn 4, `agy` tự động chạy tuần tự các lệnh sau trong terminal, tự kiểm tra mã lỗi và hoàn tất toàn bộ pipeline:

```bash
python src/analytics/survival_analysis.py
python src/models/uplift_modeling.py
python src/explainability/shap_interaction.py
python src/business_value/profit_optimization.py
python src/business_value/plot_business_insights.py
```

4. TIÊU CHÍ NGHIỆM THU HOÀN THÀNH (DEFINITION OF DONE)
   Giai đoạn 4 được coi là hoàn tất khi:
   [ ] Tệp outputs/tables/tbl_ch4_coxph_hazard_ratios.csv và tbl_ch4_survival_summary.csv được tạo đầy đủ hệ số rủi ro HR và p-value thực nghiệm.
   [ ] Tệp outputs/tables/tbl_ch4_uplift_segments_summary.csv phân loại đầy đủ 4 nhóm phản ứng tiếp thị trên tập Holdout.
   [ ] Tệp outputs/tables/tbl_ch4_shap_top_interactions.csv định lượng cụ thể các cặp tương tác phi tuyến của rào cản giỏ hàng.
   [ ] Tệp outputs/tables/tbl_ch5_threshold_optimization_results.csv xác định chính xác ngưỡng \* mang lại lợi nhuận cực đại.
   [ ] Tệp outputs/tables/tbl_ch5_decile_lift_profit.csv tính toán đầy đủ 10 phân vị Decile với Lift@K và Cumulative Gain.
   [ ] Bốn tệp ảnh fig_ch4_04_survival_cart_decay.png, fig_ch4_05_uplift_qini_curve.png, fig_ch4_06_shap_interaction_matrix.png và fig_ch5_01_expected_profit_optimization.png được kết xuất đạt chuẩn 300 DPI, đúng bảng màu quy định trong thư mục outputs/figures/.
