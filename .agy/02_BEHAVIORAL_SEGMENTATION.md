# .agy/02_BEHAVIORAL_SEGMENTATION.md

## GIAI ĐOẠN 2: PHÂN TÍCH CHUYÊN SÂU HÀNH VI GIỎ HÀNG, KIỂM ĐỊNH THỐNG KÊ VÀ PHÂN KHÚC KHÁCH HÀNG (RFM-E)

### 1. QUY TẮC THỰC THI BẮT BUỘC CHO AGENT (AGY)

1. **Tự động hóa hoàn toàn:** Agent (`agy`) đọc tài liệu này, tự động khởi tạo các module mã nguồn Python tương ứng, tự động thực thi trong môi trường cục bộ và tự động kiểm tra tính hợp lệ của các bảng số liệu, biểu đồ được xuất ra.
2. **Quy tắc bảo mật & danh tính:** Nghiêm cấm đưa tên riêng, thông tin cá nhân hay bất kỳ định danh nào vào mã nguồn, chú thích (comment) hay tên tệp. Cố định `random_state = 42`.
3. **Trung thực số liệu (Zero-Fabrication):** Mọi giá trị thống kê ($p$-value, test statistics, Silhouette score, BIC, AIC, trung bình cụm) bắt buộc phải tính toán trực tiếp từ bảng đặc trưng `data/processed/customer_features_pit.parquet`. Nghiêm cấm gán cứng giá trị giả định.
4. **Quản trị tài nguyên phần cứng (Ryzen 5 3500U, 16GB RAM):**
   - Các thuật toán phân cụm sử dụng `n_jobs = 6`.
   - Dọn dẹp bộ nhớ bằng `import gc; gc.collect()` sau mỗi công đoạn huấn luyện mô hình phân cụm.
   - Khi xử lý kiểm định thống kê trên tập dữ liệu lớn (200.000 dòng), sử dụng lấy mẫu ngẫu nhiên phân tầng có kiểm soát ($N = 10.000$ quan sát) đối với các phép kiểm định nhạy cảm về kích thước mẫu (như Shapiro-Wilk) và tính toán trên toàn bộ tập dữ liệu đối với các kiểm định phi tham số (Kruskal-Wallis, Mann-Whitney U).

---

### 2. CÁC TÁC VỤ LẬP TRÌNH VÀ THỰC THI CHI TIẾT

#### Tác vụ 2.1: Tạo và thực thi module kiểm định giả thuyết thống kê (`src/analytics/behavioral_hypothesis_testing.py`)

`agy` có nhiệm vụ tạo file `src/analytics/behavioral_hypothesis_testing.py` và chạy script để lượng hóa các rào cản chuyển đổi giỏ hàng.
Yêu cầu thuật toán và logic kiểm định:

1. **Kiểm tra tính chuẩn của phân phối (Normality Test):**
   - Áp dụng kiểm định D'Agostino-Pearson (`scipy.stats.normaltest`) trên các biến hành vi trọng tâm: `total_cart_additions`, `cart_to_page_ratio`, `cart_abandonment_severity`, `days_since_last_session`.
   - Ghi nhận bằng chứng dữ liệu có phân phối lệch phải mạnh ($p < 0.001$), khẳng định tính bắt buộc của việc sử dụng kiểm định phi tham số.
2. **Kiểm định 3 giả thuyết rào cản hành vi chuyển đổi:**
   - _Giả thuyết H1 (Rào cản ma sát giỏ hàng - Cart Friction):_
     - Câu hỏi: Nhóm khách hàng từ bỏ giỏ hàng (`cart_abandonment_severity > 0` và `target = 0`) có tỷ lệ chịu cước vận chuyển cao (`pct_overnight_shipping`) lớn hơn có ý nghĩa thống kê so với nhóm chuyển đổi thành công hay không?
     - Phương pháp: Mann-Whitney U Test (`scipy.stats.mannwhitneyu`, one-sided: `greater`).
   - _Giả thuyết H2 (Phân rã tương tác theo thời gian - Recency Decay):_
     - Câu hỏi: Mức độ tương tác giỏ hàng (`cart_velocity`) có suy giảm đáng kể theo các khoảng thời gian trôi qua kể từ phiên cuối (`days_since_last_session` chia 4 nhóm phân vị: $\le 7$ ngày, 8–15 ngày, 16–30 ngày, $> 30$ ngày) hay không?
     - Phương pháp: Kruskal-Wallis H-Test (`scipy.stats.kruskal`). Nếu $p < 0.05$, tiến hành hậu kiểm (Post-hoc) từng cặp bằng Mann-Whitney U test đi kèm hiệu chỉnh Bonferroni ($\alpha_{\text{adjusted}} = \frac{0.05}{6}$).
   - _Giả thuyết H3 (Độ nhạy khuyến mãi theo hạng hội viên - Discount Elasticity):_
     - Câu hỏi: Tỷ lệ sử dụng giảm giá (`discount_usage_rate`) có sự khác biệt có ý nghĩa giữa 4 phân hạng khách hàng (`customer_tier`: Bronze, Silver, Gold, Platinum) hay không?
     - Phương pháp: Kruskal-Wallis H-Test và Post-hoc so sánh từng cặp.
3. **Lưu trữ kết quả kiểm định:**
   - Xuất bảng kết quả ra file: `outputs/tables/tbl_ch3_hypothesis_test_results.csv` gồm các trường:
     `hypothesis_id`, `hypothesis_name`, `target_feature`, `group_variable`, `statistical_test`, `test_statistic`, `p_value`, `p_adjusted_bonferroni`, `effect_size_rank_biserial`, `conclusion`.

---

#### Tác vụ 2.2: Tạo và thực thi module phân khúc khách hàng đa chiều RFM-E (`src/analytics/customer_segmentation.py`)

`agy` có nhiệm vụ tạo file `src/analytics/customer_segmentation.py` và chạy script để phân cụm khách hàng trên không gian mở rộng RFM-Engagement-Cart.
Yêu cầu thuật toán và logic mô hình hóa:

1. **Chuẩn bị không gian đặc trưng RFM-E:**
   - Chọn 5 đặc trưng nòng cốt:
     - $R$ (Recency): `days_since_last_session`.
     - $F$ (Frequency): `trans_count`.
     - $M$ (Monetary): `total_spend`.
     - $E$ (Engagement): `total_sessions`.
     - $C$ (Cart Friction): `cart_abandonment_severity`.
   - Chuẩn hóa bằng `sklearn.preprocessing.RobustScaler` để triệt tiêu ảnh hưởng của các giá trị ngoại lai cực đoan mà không làm mất hình thái phân phối gốc.
2. **Triển khai mô hình phân cụm cơ sở (K-Means Baseline):**
   - Chạy `KMeans(random_state=42, n_init=10)` quét số cụm $k \in [3, 8]$.
   - Tính toán Silhouette Score và Davies-Bouldin Index cho từng $k$.
3. **Triển khai mô hình phân cụm nâng cao (Gaussian Mixture Models - GMM):**
   - Chạy `GaussianMixture(covariance_type='full', random_state=42, n_init=5)` quét số thành phần $k \in [3, 8]$.
   - Tính điểm Bayesian Information Criterion (BIC) và Akaike Information Criterion (AIC).
   - Chọn số cụm tối ưu $k^*$ tại điểm uốn cực tiểu của BIC.
   - Trích xuất nhãn cụm cứng (`gmm_cluster_id`) và ma trận xác suất thành viên mềm (Soft Clustering Posterior Probabilities: $P(\text{Cluster}_j \mid X_i)$).
4. **Triển khai mô hình phân cụm mật độ (HDBSCAN):**
   - Chạy `hdbscan.HDBSCAN(min_cluster_size=500, metric='euclidean', cluster_selection_method='eom')`.
   - Cô lập các quan sát nhiễu/ngoại lai (Outliers có nhãn $-1$) và tính tỷ lệ nhiễu trên tổng dân số.
5. **Định danh chân dung kinh doanh (Persona Profiling):**
   - Tính toán giá trị trung bình (mean), trung vị (median) và tỷ lệ chuyển đổi thực tế (`target`) cho từng cụm của mô hình GMM tối ưu.
   - Đặt tên cụm chuẩn hóa dựa trên insight hành vi:
     - Cụm 1: _High-Value Champions_ (Chi tiêu cao, tần suất lớn, ít bỏ rơi giỏ hàng).
     - Cụm 2: _Cart Hesitators / Shipping-Sensitive_ (Thêm giỏ nhiều, thời lượng phiên cao nhưng tỷ lệ bỏ giỏ lớn).
     - Cụm 3: _Discount Seekers_ (Tỷ lệ dùng voucher cao, đơn hàng giá trị trung bình).
     - Cụm 4: _Dormant At-Risk_ (Độ trễ phiên lớn, tương tác suy giảm mạnh).
     - Cụm 5: _Passive Browsers_ (Xem nhiều trang, ít thêm giỏ, giá trị giao dịch thấp).
6. **Lưu trữ kết quả phân khúc:**
   - Xuất bảng so sánh chỉ số giữa K-Means, GMM, HDBSCAN: `outputs/tables/tbl_ch3_clustering_metrics_comparison.csv` (gồm: `algorithm`, `k_clusters`, `silhouette_score`, `davies_bouldin_index`, `bic_score`, `outlier_ratio`, `fit_time_sec`).
   - Xuất bảng chân dung kinh doanh chi tiết: `outputs/tables/tbl_ch3_gmm_cluster_profiles.csv` (gồm: `cluster_id`, `persona_name`, `customer_count`, `pct_population`, `mean_recency`, `mean_frequency`, `mean_monetary`, `mean_cart_additions`, `mean_abandonment_severity`, `conversion_rate`).
   - Cập nhật cột `gmm_cluster_id` vào file tạm phục vụ Power BI.

---

#### Tác vụ 2.3: Tạo và thực thi script xuất biểu đồ phân khúc đạt chuẩn đồ họa học thuật (`src/analytics/plot_segmentation.py`)

`agy` có nhiệm vụ tạo file `src/analytics/plot_segmentation.py` và chạy script để xuất 3 biểu đồ chuẩn xuất bản:

- Quy chuẩn thẩm mỹ: 300 DPI, nền `#F8FAFC`, khối chính `#0F172A`, nhấn tích cực `#0D9488`, nhấn rào cản `#E11D48`, lưới phụ mờ `alpha = 0.3`, không viền trên/phải (`despine`).
  Nội dung 3 biểu đồ cần vẽ:

1. `outputs/figures/fig_ch3_03_gmm_cluster_radar.png`:
   - Biểu đồ Radar/Spider chart thể hiện hình thái 5 cụm khách hàng trên 5 trục đặc trưng chuẩn hóa ($[0, 1]$ qua Min-Max Scaling phục vụ vẽ radar): Recency, Frequency, Monetary, Sessions, Cart Abandonment.
   - Chú giải rõ ràng từng màu tương ứng với từng Persona kinh doanh.
2. `outputs/figures/fig_ch3_04_cart_friction_by_cluster.png`:
   - Biểu đồ Boxplot kết hợp dải điểm mờ (strip/jitter plot) phân tích sự phân hóa của biến `cart_abandonment_severity` giữa 5 cụm.
   - Thêm Annotation Callout chỉ rõ cụm _Cart Hesitators_ có mức độ nghiêm trọng vượt trội so với các cụm còn lại.
3. `outputs/figures/fig_ch3_05_gmm_bic_aic_selection.png`:
   - Đồ thị đường kép so sánh giá trị BIC (đường màu `#0F172A`) và AIC (đường màu `#0D9488`) khi quét số thành phần $k \in [3, 8]$.
   - Có đường gióng nét đứt màu đỏ `#E11D48` tại điểm $k^*$ được chọn làm số cụm tối ưu.

---

### 3. QUY TRÌNH THỰC THI TỰ ĐỘNG CHO AGENT

Khi kích hoạt giai đoạn 2, `agy` chạy tuần tự trong terminal:

```bash
python src/analytics/behavioral_hypothesis_testing.py
python src/analytics/customer_segmentation.py
python src/analytics/plot_segmentation.py

4. TIÊU CHÍ NGHIỆM THU HOÀN THÀNH (DEFINITION OF DONE)
Giai đoạn 2 hoàn thành khi và chỉ khi:

File outputs/tables/tbl_ch3_hypothesis_test_results.csv được sinh ra, ghi nhận đầy đủ thống kê của 3 giả thuyết với
p-value thực tế.

File outputs/tables/tbl_ch3_clustering_metrics_comparison.csv so sánh đầy đủ 3 thuật toán K-Means, GMM, HDBSCAN.

File outputs/tables/tbl_ch3_gmm_cluster_profiles.csv mô tả chi tiết 5 chân dung khách hàng kèm tỷ lệ chuyển đổi thực tế.

Ba file hình ảnh fig_ch3_03_gmm_cluster_radar.png, fig_ch3_04_cart_friction_by_cluster.png, fig_ch3_05_gmm_bic_aic_selection.png nằm trong thư mục outputs/figures/, đạt chuẩn 300 DPI và tuân thủ bảng màu quy định.
```
