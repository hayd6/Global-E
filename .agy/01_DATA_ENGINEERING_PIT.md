# .agy/01_DATA_ENGINEERING_PIT.md

## CHỈ DẪN THỰC THI CHO AGENT (AGY) - GIAI ĐOẠN 1: DATA HEALING VÀ TRÍCH XUẤT FEATURE STORE POINT-IN-TIME (PIT)

### 1. QUY TẮC BẮT BUỘC KHI THỰC THI

1. **Tuân thủ vai trò:** Agent (`agy`) đọc tài liệu này, tự động khởi tạo mã nguồn, tự động thực thi các file Python bằng môi trường cục bộ và tự động kiểm tra kết quả thông qua bài test `pytest`. Không yêu cầu người dùng thao tác thủ công.
2. **Quy tắc bảo mật & danh tính:** Tuyệt đối không chèn bất kỳ tên riêng của người dùng hay thông tin cá nhân vào code, cấu hình, log hay tên file. Cố định `random_state = 42`.
3. **Trung thực dữ liệu (Zero-Fabrication):** Mọi số liệu trong các bảng kiểm toán và biểu đồ phải được tính toán trực tiếp từ dữ liệu thực tế bằng DuckDB/Python. Nghiêm cấm tạo số liệu giả định.
4. **Quản trị tài nguyên phần cứng (Ryzen 5 3500U, 16GB RAM):**
   - Thiết lập bắt buộc trong DuckDB: `SET threads = 6; SET max_memory = '10GB';`.
   - Giải phóng bộ nhớ tường minh: `import gc; gc.collect()` sau mỗi phép tính toán bảng lớn.
   - Ép kiểu dữ liệu tối ưu: `float32`, `int32`, `int8`, `category` để tiết kiệm RAM.

---

### 2. CÁC TÁC VỤ LẬP TRÌNH VÀ THỰC THI CỤ THỂ

#### Tác vụ 1.1: Tạo và thực thi module sửa lỗi dữ liệu (`src/data_engineering/data_healing.py`)

`agy` có nhiệm vụ tạo file `src/data_engineering/data_healing.py` và chạy script này để xử lý 8 file CSV trong `data/raw/` bằng DuckDB SQL.
Yêu cầu thuật toán và logic:

1. **Khắc phục lỗi đảo ngược thời gian (Temporal Inconsistency):**
   - Kết nối `sessions.csv` và `transactions.csv` với `customers.csv` qua `customer_id`.
   - Lọc bỏ các bản ghi có `session_start_time < registration_date` hoặc `transaction_timestamp < registration_date`.
2. **Khắc phục lỗi logic giao dịch:**
   - Lọc bỏ các bản ghi giao dịch có `items_count <= 0` nhưng `order_value > 0`.
3. **Chuẩn hóa trường dữ liệu:**
   - Trường `order_value`: Loại bỏ ký tự tiền tệ (`$`, `,`), ép kiểu sang `DOUBLE`.
   - Trường `bounce_flag` và `discount_applied`: Chuẩn hóa các dạng chuỗi (`Yes`/`No`, `TRUE`/`FALSE`, `1`/`0`) về số nguyên nhị phân `{0, 1}`.
   - Trường `age`: Chuyển đổi các giá trị không hợp lệ (`unknown`, số âm, $> 100$) thành `NULL`, sau đó tính toán và điền bằng giá trị trung vị (median) của nhóm `customer_tier` tương ứng.
4. **Lưu trữ kết quả kiểm toán:**
   - Xuất bảng thống kê kết quả làm sạch ra file: `outputs/tables/tbl_ch1_data_healing_audit.csv` gồm các cột:
     `table_name`, `raw_row_count`, `healed_row_count`, `anomalies_removed`, `timestamp_violations_fixed`.

---

#### Tác vụ 1.2: Tạo và thực thi module trích xuất Feature Store Point-in-Time (`src/data_engineering/build_features_pit.py`)

`agy` có nhiệm vụ tạo file `src/data_engineering/build_features_pit.py` và chạy script này để tổng hợp dữ liệu sạch thành bảng đặc trưng cấp khách hàng (1 dòng = 1 khách hàng) tại mốc chốt thời gian $t_0$.
Yêu cầu thuật toán và logic:

1. **Thiết lập ranh giới Point-in-Time (PIT):**
   - Đọc mốc `cutoff_date` ($t_0$) từ `configs/base_config.yaml` (mặc định: `2024-06-01`).
   - Khoảng quan sát tính toán đặc trưng ($X$): Toàn bộ sự kiện có mốc thời gian $\le t_0$.
   - Khoảng xác định nhãn mục tiêu ($target$): Cửa sổ 30 ngày sau mốc chốt ($t_0 < \text{timestamp} \le t_0 + 30\text{ ngày}$).
   - Logic tạo nhãn: Khách hàng có $\ge 1$ giao dịch hợp lệ trong cửa sổ này $\rightarrow target = 1$, ngược lại $target = 0$.
2. **Trích xuất nhóm đặc trưng hành vi và rào cản giỏ hàng:**
   Thực hiện truy vấn gom nhóm (`GROUP BY customer_id`) trên phạm vi dữ liệu $\le t_0$:
   - _Đặc trưng tương tác và rào cản giỏ hàng:_
     - `total_cart_additions`: Tổng lượt nhấn thêm giỏ hàng ($\sum \text{cart\_additions}$).
     - `cart_to_page_ratio`: $\frac{\text{total\_cart\_additions}}{\text{total\_pages\_viewed} + 1}$.
     - `cart_abandonment_severity`: Số phiên có $\text{cart\_additions} > 0$ nhưng không có giao dịch trong phiên.
     - `abandonment_ratio`: $\frac{\text{cart\_abandonment\_severity}}{\text{total\_sessions} + 1}$.
     - `cart_velocity`: Số lượt thêm giỏ hàng trung bình trên mỗi phiên hoạt động.
     - `hesitation_index`: $\frac{\text{total\_duration\_sec}}{\text{total\_cart\_additions} + 1}$ (thời gian cân nhắc cho mỗi lần thêm giỏ).
   - _Đặc trưng phân rã thời gian (Recency Decay):_
     - `days_since_last_session`: $t_0 - \max(\text{session\_start\_time})$ (tính bằng ngày).
     - `days_since_last_purchase`: $t_0 - \max(\text{transaction\_timestamp})$ (nếu chưa từng mua hàng thì điền $999$).
     - `activity_trend_slope`: Tỷ số giữa số phiên trong 15 ngày sát mốc $t_0$ so với 15 ngày liền trước đó.
   - _Đặc trưng ma sát vận chuyển và nhạy cảm giá:_
     - `discount_usage_rate`: Tỷ lệ giao dịch lịch sử có sử dụng giảm giá.
     - `pct_overnight_shipping`: Tỷ lệ giao dịch chọn phương thức giao hàng qua đêm/hỏa tốc.
     - `shipping_friction_score`: $\text{abandonment\_ratio} \times \text{pct\_overnight\_shipping}$.
     - `pct_campaign_sessions`: Tỷ lệ phiên truy cập bắt nguồn từ các chiến dịch tiếp thị.
   - _Đặc trưng hồ sơ và kinh tế - xã hội:_
     - Ghép thông tin từ `customers.csv` và `geo_data.csv`: `age`, `account_age_days` (tính tới $t_0$), `customer_tier_code` (Bronze=1, Silver=2, Gold=3, Platinum=4), `loyalty_score`, `credit_limit`, `average_income`, `urban_ratio`.
3. **Lưu trữ dữ liệu:**
   - Lưu trữ toàn bộ bảng đặc trưng của 200.000 khách hàng ra file:
     `data/processed/customer_features_pit.parquet` (nén Snappy, kiểu dữ liệu tối ưu: `float32`, `int32`).
   - Xuất file mẫu 5.000 dòng để phục vụ kiểm tra: `outputs/tables/customer_features_pit_sample.csv`.
   - Xuất từ điển đặc trưng thực tế ra file: `outputs/tables/tbl_ch3_feature_dictionary.csv` gồm các cột:
     `feature_name`, `data_type`, `category`, `formula`, `business_meaning`.

---

#### Tác vụ 1.3: Tạo và thực thi kiểm thử tự động (`tests/test_pit_integrity.py`)

`agy` có nhiệm vụ tạo file `tests/test_pit_integrity.py` và chạy lệnh kiểm thử bằng `pytest`:

1. `test_unique_customer_id()`: Khẳng định trường `customer_id` không có bản ghi trùng lặp trong tệp `.parquet`.
2. `test_feature_exclusion()`: Khẳng định các trường `customer_id` và `target` tuyệt đối không nằm trong danh sách các biến đặc trưng $X$.
3. `test_temporal_invariance()`:
   - Trích xuất ngẫu nhiên mẫu 100 khách hàng từ cơ sở dữ liệu.
   - Bổ sung 50 bản ghi giao dịch nhân tạo với mốc thời gian sau $t_0$ ($t > t_0$).
   - Tính toán lại ma trận đặc trưng tại mốc $t_0$.
   - Dùng `pandas.testing.assert_frame_equal` để khẳng định toàn bộ giá trị đặc trưng tính tại $t_0$ không hề bị thay đổi trước và sau khi bổ sung dữ liệu tương lai.

---

#### Tác vụ 1.4: Tạo và thực thi script xuất biểu đồ kiểm toán phân phối (`src/data_engineering/plot_pit_audit.py`)

`agy` có nhiệm vụ tạo file `src/data_engineering/plot_pit_audit.py` và chạy script để kết xuất hình ảnh đạt tiêu chuẩn đồ họa xuất bản:

- Quy chuẩn thẩm mỹ: Nền `#F8FAFC`, Khối chính `#0F172A`, Nhấn chuyển đổi `#0D9488`, Nhấn rào cản `#E11D48`.
- Độ phân giải: 300 DPI, font chữ sans-serif, loại bỏ viền trên/phải (`despine`), lưới phụ mờ `alpha = 0.3`.
  Nội dung 2 biểu đồ cần vẽ:

1. `outputs/figures/fig_ch3_01_target_distribution.png`:
   - Biểu đồ cột thể hiện phân phối nhãn chuyển đổi ($target = 0$ và $target = 1$).
   - Ghi trực tiếp tỷ lệ phần trăm (%) và số lượng khách hàng thực tế trên đầu mỗi cột.
   - Tiêu đề chính nêu rõ tỷ lệ mất cân bằng, phụ đề nêu rõ cửa sổ nhãn 30 ngày sau mốc $t_0$.
2. `outputs/figures/fig_ch3_02_cart_engagement_scatter.png`:
   - Biểu đồ phân tán (Scatter plot) thể hiện mối liên hệ giữa `total_pages_viewed` (trục hoành) và `total_cart_additions` (trục tung).
   - Phân màu theo nhãn $target$ (Xanh ngọc cho chuyển đổi, Đỏ san hô cho từ bỏ giỏ hàng).
   - Vẽ đường nét đứt và thêm khung chú thích (Annotation Callout) chỉ ra vùng mật độ cao của nhóm khách hàng "Xem nhiều trang, Thêm nhiều sản phẩm vào giỏ nhưng không chuyển đổi".

---

### 3. QUY TRÌNH THỰC THI TỰ ĐỘNG CHO AGENT

Khi nhận lệnh, `agy` phải tự động chạy tuần tự các lệnh sau trong terminal, bắt lỗi và chỉ dừng lại khi tất cả hoàn tất:

```bash
python src/data_engineering/data_healing.py
python src/data_engineering/build_features_pit.py
pytest tests/test_pit_integrity.py
python src/data_engineering/plot_pit_audit.py
```

4. TIÊU CHÍ NGHIỆM THU HOÀN THÀNH (DEFINITION OF DONE)
   Giai đoạn 1 hoàn thành khi và chỉ khi:

Tệp outputs/tables/tbl_ch1_data_healing_audit.csv được sinh ra với đầy đủ thống kê xử lý lỗi.

Tệp data/processed/customer_features_pit.parquet được tạo đầy đủ 200.000 dòng, kích thước file tối ưu, không phát sinh lỗi tràn RAM 16GB.

Tệp outputs/tables/tbl_ch3_feature_dictionary.csv mô tả đầy đủ ít nhất 40 đặc trưng được trích xuất.

Lệnh kiểm thử pytest tests/test_pit_integrity.py đạt kết quả 100% Passed.

Hai tệp ảnh outputs/figures/fig_ch3_01_target_distribution.png và outputs/figures/fig_ch3_02_cart_engagement_scatter.png được tạo với độ phân giải 300 DPI, có đầy đủ tiêu đề và chú thích nghiệp vụ.
