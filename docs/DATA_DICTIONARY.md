# TỪ ĐIỂN DỮ LIỆU CHUẨN HÓA (DATA DICTIONARY)

Tài liệu này định nghĩa chi tiết cấu trúc, kiểu dữ liệu, ý nghĩa nghiệp vụ và quy tắc tiền xử lý cho toàn bộ các trường dữ liệu trong dự án: từ 8 bảng dữ liệu thô (Raw Data), bảng đặc trưng Point-in-Time (Feature Store) đến các bảng dữ liệu mô hình hình sao (Star Schema) phục vụ Power BI.

---

## 1. DỮ LIỆU THÔ ĐẦU VÀO (`data/raw/`)

### 1.1. Bảng `customers.csv` (Hồ sơ khách hàng - 200.000 dòng)

| Tên cột               | Kiểu dữ liệu gốc    | Kiểu chuẩn hóa | Ràng buộc / Miền giá trị               | Mô tả nghiệp vụ                       | Quy tắc xử lý dữ liệu lỗi                                                                 |
| :-------------------- | :------------------ | :------------- | :------------------------------------- | :------------------------------------ | :---------------------------------------------------------------------------------------- |
| `customer_id`         | `VARCHAR`           | `VARCHAR`      | Khóa chính (PK), Unique                | Mã định danh duy nhất của khách hàng  | Bắt buộc có, không trùng lặp                                                              |
| `age`                 | `VARCHAR` / `FLOAT` | `INT32`        | $[18, 100]$                            | Tuổi của khách hàng                   | Giá trị `unknown`, âm hoặc $>100$ chuyển thành `NULL`, điền trung vị theo `customer_tier` |
| `gender`              | `VARCHAR`           | `CATEGORY`     | `Male`, `Female`, `Other`              | Giới tính khách hàng                  | Chuẩn hóa chữ thường/hoa, điền `Unknown` nếu khuyết                                       |
| `country`             | `VARCHAR`           | `CATEGORY`     | Mã quốc gia ISO                        | Quốc gia cư trú                       | Điền `Unknown` nếu khuyết                                                                 |
| `registration_date`   | `VARCHAR`           | `DATE`         | $\le t_0$                              | Ngày đăng ký tài khoản                | Chuyển định dạng `YYYY-MM-DD`, dùng làm mốc chặn dưới cho phiên và giao dịch              |
| `customer_tier`       | `VARCHAR`           | `CATEGORY`     | `Bronze`, `Silver`, `Gold`, `Platinum` | Phân hạng hội viên                    | Mã hóa thứ bậc (Ordinal: 1, 2, 3, 4) hoặc One-Hot                                         |
| `loyalty_score`       | `FLOAT`             | `FLOAT32`      | $[0.0, 1.0]$                           | Điểm tích lũy lòng trung thành        | Clip trong khoảng $[0, 1]$, điền trung vị nếu khuyết                                      |
| `credit_limit`        | `FLOAT`             | `FLOAT32`      | $\ge 0$                                | Hạn mức tín dụng được cấp (USD)       | Điền trung vị nếu khuyết                                                                  |
| `email_open_rate`     | `FLOAT`             | `FLOAT32`      | $[0.0, 1.0]$                           | Tỷ lệ mở email tiếp thị               | Điền $0.0$ nếu khuyết (giả định chưa từng mở)                                             |
| `discount_usage_rate` | `FLOAT`             | `FLOAT32`      | $[0.0, 1.0]$                           | Tỷ lệ giao dịch từng dùng giảm giá    | Điền $0.0$ nếu chưa từng giao dịch                                                        |
| `referral_code`       | `VARCHAR`           | `INT8`         | $0$ hoặc $1$                           | Khách hàng có mã giới thiệu hay không | Chuỗi rỗng hoặc `NULL` $\rightarrow 0$; có mã $\rightarrow 1$                             |
| `review_score`        | `FLOAT`             | `FLOAT32`      | $[1.0, 5.0]$                           | Điểm đánh giá trung bình của khách    | Điền trung bình chung hoặc tạo nhãn riêng nếu khuyết                                      |

---

### 1.2. Bảng `sessions.csv` (Nhật ký phiên truy cập - 2.000.000 dòng)

| Tên cột                | Kiểu dữ liệu gốc    | Kiểu chuẩn hóa | Ràng buộc / Miền giá trị                              | Mô tả nghiệp vụ                             | Quy tắc xử lý dữ liệu lỗi                                                        |
| :--------------------- | :------------------ | :------------- | :---------------------------------------------------- | :------------------------------------------ | :------------------------------------------------------------------------------- |
| `session_id`           | `VARCHAR`           | `VARCHAR`      | Khóa chính (PK), Unique                               | Mã định danh duy nhất của phiên             | Bắt buộc có                                                                      |
| `customer_id`          | `VARCHAR`           | `VARCHAR`      | Khóa ngoại (FK)                                       | Mã khách hàng thực hiện phiên               | Tham chiếu `customers.customer_id`                                               |
| `session_start_time`   | `VARCHAR`           | `TIMESTAMP`    | Thời gian                                             | Thời điểm bắt đầu phiên truy cập            | Chuyển sang `TIMESTAMP`. Bỏ phiên nếu $< \text{registration\_date}$              |
| `session_duration_sec` | `FLOAT`             | `INT32`        | $\ge 0$                                               | Tổng thời lượng phiên (giây)                | Âm chuyển thành `NULL` $\rightarrow$ điền trung vị                               |
| `pages_viewed`         | `VARCHAR` / `FLOAT` | `INT32`        | $\ge 1$                                               | Số trang đã xem trong phiên                 | Giá trị `N/A` hoặc $\le 0$ chuyển thành $1$                                      |
| `cart_additions`       | `INT`               | `INT32`        | $\ge 0$                                               | Số lượt nhấn thêm sản phẩm vào giỏ          | Điền $0$ nếu khuyết                                                              |
| `bounce_flag`          | `VARCHAR`           | `INT8`         | $0$ hoặc $1$                                          | Phiên thoát trang (chỉ xem 1 trang rồi rời) | Chuẩn hóa `Yes`, `1`, `TRUE` $\rightarrow 1$; `No`, `0`, `FALSE` $\rightarrow 0$ |
| `traffic_source`       | `VARCHAR`           | `CATEGORY`     | `Direct`, `Organic`, `Paid Search`, `Social`, `Email` | Kênh nguồn dẫn truy cập                     | Chuẩn hóa danh mục, nhóm các giá trị hiếm vào `Other`                            |
| `device_category`      | `VARCHAR`           | `CATEGORY`     | `Mobile`, `Desktop`, `Tablet`                         | Loại thiết bị truy cập                      | Chuẩn hóa danh mục                                                               |
| `campaign_id`          | `VARCHAR`           | `VARCHAR`      | Khóa ngoại (FK)                                       | Mã chiến dịch marketing kích hoạt phiên     | Giá trị `none`, rỗng chuyển thành `NULL`                                         |
| `geo_ip_region`        | `VARCHAR`           | `VARCHAR`      | Khóa ngoại (FK)                                       | Khu vực địa lý định vị qua IP               | Tham chiếu `geo_data.geo_ip_region`                                              |

---

### 1.3. Bảng `transactions.csv` (Lịch sử giao dịch - 500.000 dòng)

| Tên cột                 | Kiểu dữ liệu gốc | Kiểu chuẩn hóa | Ràng buộc / Miền giá trị                              | Mô tả nghiệp vụ                      | Quy tắc xử lý dữ liệu lỗi                                                     |
| :---------------------- | :--------------- | :------------- | :---------------------------------------------------- | :----------------------------------- | :---------------------------------------------------------------------------- |
| `transaction_id`        | `VARCHAR`        | `VARCHAR`      | Khóa chính (PK), Unique                               | Mã định danh đơn hàng giao dịch      | Bắt buộc có                                                                   |
| `customer_id`           | `VARCHAR`        | `VARCHAR`      | Khóa ngoại (FK)                                       | Mã khách hàng thực hiện giao dịch    | Tham chiếu `customers.customer_id`                                            |
| `transaction_timestamp` | `VARCHAR`        | `TIMESTAMP`    | Thời gian                                             | Thời điểm thanh toán đơn hàng        | Chuyển `TIMESTAMP`. Bỏ giao dịch nếu $< \text{registration\_date}$            |
| `order_value`           | `VARCHAR`        | `FLOAT32`      | $> 0$                                                 | Tổng giá trị đơn hàng (USD)          | Xóa ký tự tiền tệ (`$`, `,`), ép kiểu `FLOAT`. Âm hoặc $= 0$ chuyển `NULL`    |
| `items_count`           | `INT`            | `INT32`        | $\ge 1$                                               | Số lượng sản phẩm trong đơn          | Bỏ các bản ghi có $\text{items\_count} \le 0$ nhưng $\text{order\_value} > 0$ |
| `payment_method`        | `VARCHAR`        | `CATEGORY`     | `Credit Card`, `Debit Card`, `PayPal`, `COD`, `Other` | Phương thức thanh toán               | Chuẩn hóa danh mục                                                            |
| `discount_applied`      | `VARCHAR`        | `INT8`         | $0$ hoặc $1$                                          | Đơn hàng có áp dụng mã giảm giá      | Chuẩn hóa các dạng chuỗi thành $\{0, 1\}$                                     |
| `shipping_method`       | `VARCHAR`        | `CATEGORY`     | `Standard`, `Express`, `Overnight`                    | Phương thức giao hàng                | Yếu tố phản ánh ma sát chi phí vận chuyển                                     |
| `high_value_flag`       | `INT`            | `INT8`         | $0$ hoặc $1$                                          | Giao dịch có giá trị cao vượt ngưỡng | Kiểm tra tính nhất quán với `order_value`                                     |

---

### 1.4. Bảng `marketing_campaigns.csv` (Chiến dịch tiếp thị - 200 dòng)

| Tên cột         | Kiểu chuẩn hóa | Mô tả nghiệp vụ                                                     |
| :-------------- | :------------- | :------------------------------------------------------------------ |
| `campaign_id`   | `VARCHAR` (PK) | Mã định danh chiến dịch                                             |
| `campaign_name` | `VARCHAR`      | Tên chiến dịch tiếp thị                                             |
| `channel`       | `CATEGORY`     | Kênh phân phối chiến dịch (`Google Ads`, `Meta Ads`, `Email`, v.v.) |
| `start_date`    | `DATE`         | Ngày bắt đầu chiến dịch                                             |
| `end_date`      | `DATE`         | Ngày kết thúc chiến dịch                                            |
| `budget`        | `FLOAT32`      | Ngân sách phân bổ cho chiến dịch (USD)                              |

---

### 1.5. Bảng `geo_data.csv` (Đặc trưng địa lý kinh tế - 100 dòng)

| Tên cột                | Kiểu chuẩn hóa | Miền giá trị | Mô tả nghiệp vụ                                 |
| :--------------------- | :------------- | :----------- | :---------------------------------------------- |
| `geo_ip_region`        | `VARCHAR` (PK) | Mã vùng IP   | Khóa liên kết vùng địa lý                       |
| `region_name`          | `VARCHAR`      | Tên khu vực  | Tên tỉnh/bang/khu vực                           |
| `average_income`       | `FLOAT32`      | $> 0$        | Thu nhập bình quân của dân cư khu vực (USD/năm) |
| `urban_ratio`          | `FLOAT32`      | $[0.0, 1.0]$ | Tỷ lệ đô thị hóa tại khu vực                    |
| `internet_penetration` | `FLOAT32`      | $[0.0, 1.0]$ | Tỷ lệ phủ sóng internet băng thông rộng         |

---

### 1.6. Bảng `train.csv` & `test.csv` (Nhãn và tập nộp bài)

- `train.csv`:
  - `customer_id` (`VARCHAR`, PK): Mã định danh khách hàng thuộc tập huấn luyện (160.000 dòng).
  - `target` (`INT8`): Nhãn mục tiêu nhị phân ($1$: Khách hàng có phát sinh giao dịch mua hàng; $0$: Không phát sinh).
- `test.csv`:
  - `customer_id` (`VARCHAR`, PK): Danh sách mã khách hàng cần xuất dự đoán xác suất (40.000 dòng).

---

## 2. BẢNG ĐẶC TRƯNG POINT-IN-TIME (`customer_features_pit.parquet`)

Toàn bộ đặc trưng được tính tại mốc chốt cutoff $t_0$, chỉ sử dụng các sự kiện $\le t_0$. Đơn vị phân tích: 1 dòng = 1 khách hàng.

### 2.1. Nhóm đặc trưng hồ sơ nền tảng (Demographic & Account Basics)

| Tên đặc trưng        | Kiểu      | Công thức / Định nghĩa                         | Ý nghĩa phân tích                |
| :------------------- | :-------- | :--------------------------------------------- | :------------------------------- |
| `age`                | `INT32`   | Tuổi khách hàng                                | Nhân khẩu học cơ bản             |
| `account_age_days`   | `INT32`   | $t_0 - \text{registration\_date}$              | Độ tuổi tài khoản tính bằng ngày |
| `customer_tier_code` | `INT8`    | `Bronze`=1, `Silver`=2, `Gold`=3, `Platinum`=4 | Hạng thành viên dạng thứ bậc     |
| `loyalty_score`      | `FLOAT32` | Điểm tích lũy trung thành                      | Mức độ gắn kết thương hiệu       |
| `credit_limit`       | `FLOAT32` | Hạn mức tín dụng                               | Năng lực tài chính khả dụng      |

### 2.2. Nhóm đặc trưng cường độ tương tác phiên (Digital Engagement)

| Tên đặc trưng             | Kiểu      | Công thức / Định nghĩa                                                           | Ý nghĩa phân tích                 |
| :------------------------ | :-------- | :------------------------------------------------------------------------------- | :-------------------------------- |
| `total_sessions`          | `INT32`   | $\sum \mathbb{I}(\text{session} \le t_0)$                                        | Tần suất ghé thăm website         |
| `total_duration_sec`      | `FLOAT32` | $\sum \text{session\_duration\_sec}$                                             | Tổng thời lượng tương tác         |
| `avg_session_duration`    | `FLOAT32` | $\frac{\text{total\_duration\_sec}}{\text{total\_sessions}}$                     | Độ sâu quan tâm trong mỗi phiên   |
| `total_pages_viewed`      | `INT32`   | $\sum \text{pages\_viewed}$                                                      | Khối lượng nội dung đã duyệt      |
| `avg_pages_per_session`   | `FLOAT32` | $\frac{\text{total\_pages\_viewed}}{\text{total\_sessions}}$                     | Khả năng tìm kiếm hàng hóa        |
| `bounce_rate`             | `FLOAT32` | $\frac{\sum \text{bounce\_flag}}{\text{total\_sessions}}$                        | Tỷ lệ không tương tác sâu         |
| `days_since_last_session` | `INT32`   | $t_0 - \max(\text{session\_start\_time})$                                        | Độ trễ tương tác (Recency phiên)  |
| `activity_trend_slope`    | `FLOAT32` | $\frac{\text{Sessions}_{[t_0-15, t_0]}}{\text{Sessions}_{[t_0-30, t_0-15]} + 1}$ | Gia tốc tương tác gần mốc dự đoán |

### 2.3. Nhóm rào cản và hành vi giỏ hàng (Cart Barrier & Friction Indicators - Trọng tâm)

| Tên đặc trưng               | Kiểu      | Công thức / Định nghĩa                                                            | Ý nghĩa phân tích rào cản                                                 |
| :-------------------------- | :-------- | :-------------------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| `total_cart_additions`      | `INT32`   | $\sum \text{cart\_additions}$                                                     | Tổng số sản phẩm đưa vào giỏ                                              |
| `cart_to_page_ratio`        | `FLOAT32` | $\frac{\text{total\_cart\_additions}}{\text{total\_pages\_viewed} + 1}$           | Mức độ tập trung vào ý định mua thay vì lướt xem                          |
| `cart_velocity`             | `FLOAT32` | $\frac{\text{total\_cart\_additions}}{\text{total\_sessions}}$                    | Tốc độ đưa hàng vào giỏ mỗi phiên                                         |
| `cart_abandonment_severity` | `INT32`   | $\sum \mathbb{I}(\text{cart\_additions} > 0 \land \text{no\_trans\_in\_session})$ | **Chỉ số bỏ rơi giỏ hàng**: Số phiên có ý định mua nhưng không thanh toán |
| `abandonment_ratio`         | `FLOAT32` | $\frac{\text{cart\_abandonment\_severity}}{\text{total\_sessions}}$               | Tỷ lệ phiên bỏ rơi giỏ hàng                                               |
| `hesitation_index`          | `FLOAT32` | $\frac{\text{total\_duration\_sec}}{\text{total\_cart\_additions} + 1}$           | Thời gian cân nhắc cho mỗi lần thêm giỏ                                   |

### 2.4. Nhóm lịch sử thanh toán & ma sát vận chuyển (Transaction & Friction)

| Tên đặc trưng              | Kiểu      | Công thức / Định nghĩa                                                          | Ý nghĩa phân tích rào cản                          |
| :------------------------- | :-------- | :------------------------------------------------------------------------------ | :------------------------------------------------- |
| `trans_count`              | `INT32`   | $\sum \mathbb{I}(\text{transaction} \le t_0)$                                   | Tần suất mua hàng quá khứ                          |
| `total_spend`              | `FLOAT32` | $\sum \text{order\_value}$                                                      | Tổng giá trị chi tiêu lịch sử                      |
| `avg_order_value`          | `FLOAT32` | $\frac{\text{total\_spend}}{\text{trans\_count}}$                               | Kích thước giỏ hàng tiền tệ (AOV)                  |
| `days_since_last_purchase` | `INT32`   | $t_0 - \max(\text{transaction\_timestamp})$                                     | Độ trễ giao dịch (RFM Recency)                     |
| `discount_usage_rate`      | `FLOAT32` | $\frac{\sum \text{discount\_applied}}{\text{trans\_count}}$                     | Độ nhạy cảm với khuyến mãi                         |
| `pct_overnight_shipping`   | `FLOAT32` | $\frac{\sum \mathbb{I}(\text{shipping}=\text{Overnight})}{\text{trans\_count}}$ | Tỷ lệ chấp nhận cước vận chuyển cao                |
| `shipping_friction_score`  | `FLOAT32` | $\text{abandonment\_ratio} \times \text{pct\_overnight\_shipping}$              | **Tương tác ma sát**: Bỏ giỏ do phí vận chuyển cao |

### 2.5. Nhóm ngữ cảnh kênh và vùng địa lý (Contextual Features)

| Tên đặc trưng           | Kiểu      | Công thức / Định nghĩa                                                            | Ý nghĩa phân tích              |
| :---------------------- | :-------- | :-------------------------------------------------------------------------------- | :----------------------------- |
| `pct_mobile_sessions`   | `FLOAT32` | $\frac{\text{Mobile Sessions}}{\text{total\_sessions}}$                           | Thói quen mua sắm di động      |
| `pct_desktop_sessions`  | `FLOAT32` | $\frac{\text{Desktop Sessions}}{\text{total\_sessions}}$                          | Thói quen mua sắm máy tính bàn |
| `pct_campaign_sessions` | `FLOAT32` | $\frac{\sum \mathbb{I}(\text{campaign\_id is not null})}{\text{total\_sessions}}$ | Mức độ phụ thuộc vào quảng cáo |
| `average_income`        | `FLOAT32` | Thu nhập bình quân vùng IP                                                        | Năng lực chi tiêu khu vực      |
| `urban_ratio`           | `FLOAT32` | Tỷ lệ đô thị hóa vùng IP                                                          | Hạ tầng logistics tiếp cận     |

---

## 3. MÔ HÌNH DỮ LIỆU POWER BI (STAR SCHEMA - `outputs/powerbi/`)

### 3.1. Bảng `fact_customer_decisions.csv` (Bảng Fact trung tâm - 200.000 dòng)

| Tên cột                     | Kiểu      | Vai trò                 | Mô tả nghiệp vụ                                                                 |
| :-------------------------- | :-------- | :---------------------- | :------------------------------------------------------------------------------ |
| `customer_id`               | `VARCHAR` | Khóa chính / Khóa ngoại | Mã định danh khách hàng liên kết các Dim                                        |
| `target_actual`             | `INT8`    | Đo lường (Measure)      | Nhãn thực tế ($1$: Mua, $0$: Không mua, `NULL` cho tập Test)                    |
| `predicted_prob_calibrated` | `FLOAT32` | Đo lường (Measure)      | Xác suất chuyển đổi sau hiệu chỉnh Isotonic/Platt                               |
| `decision_optimal_tau`      | `INT8`    | Đo lường (Measure)      | Quyết định can thiệp tại ngưỡng tối ưu $\tau^*$ ($1$ nếu $p \ge \tau^*$)        |
| `uplift_score`              | `FLOAT32` | Đo lường (Measure)      | Điểm số tác động gia tăng của tiếp thị: $\tau_i = \mathbb{E}[Y(1)-Y(0)]$        |
| `uplift_segment`            | `VARCHAR` | Chiều phân tích         | Phân loại 4 nhóm: `Persuadables`, `Sure Things`, `Lost Causes`, `Sleeping Dogs` |
| `gmm_cluster_id`            | `INT8`    | Chiều phân tích         | Cụm phân khúc hành vi GMM ($1$ đến $5$)                                         |
| `clv_predicted_usd`         | `FLOAT32` | Đo lường (Measure)      | Giá trị vòng đời dự báo (USD)                                                   |
| `expected_margin_usd`       | `FLOAT32` | Đo lường (Measure)      | Lợi nhuận biên dự kiến: $25\% \times \text{AOV}$                                |
| `expected_net_profit_usd`   | `FLOAT32` | Đo lường (Measure)      | Lợi nhuận ròng dự kiến sau khi trừ chi phí tiếp cận                             |
| `decile_rank`               | `INT8`    | Phân vị ($1$ đến $10$)  | Xếp hạng Decile theo xác suất giảm dần ($1$ là top 10% cao nhất)                |

### 3.2. Bảng `dim_customers.csv` (Chiều thông tin khách hàng)

- `customer_id` (`VARCHAR`, PK)
- `age_group` (`CATEGORY`: `<25`, `25-34`, `35-44`, `45-54`, `55+`)
- `gender` (`CATEGORY`)
- `country` (`CATEGORY`)
- `customer_tier` (`CATEGORY`: `Bronze`, `Silver`, `Gold`, `Platinum`)
- `loyalty_score` (`FLOAT32`)
- `credit_limit_tier` (`CATEGORY`: `Low`, `Medium`, `High`, `VIP`)

### 3.3. Bảng `dim_cart_behavior.csv` (Chiều chi tiết hành vi giỏ hàng)

- `customer_id` (`VARCHAR`, PK)
- `cart_abandonment_severity` (`INT32`)
- `cart_to_page_ratio` (`FLOAT32`)
- `cart_velocity` (`FLOAT32`)
- `hesitation_index` (`FLOAT32`)
- `primary_device` (`CATEGORY`: `Mobile`, `Desktop`, `Tablet`)
- `primary_traffic_source` (`CATEGORY`)
- `abandonment_risk_level` (`CATEGORY`: `Low`, `Medium`, `High`, `Severe`)

### 3.4. Bảng `dim_threshold_simulation.csv` (Chiều mô phỏng ngưỡng tài chính - 100 dòng)

| Tên cột                   | Kiểu           | Mô tả                                                                                                |
| :------------------------ | :------------- | :--------------------------------------------------------------------------------------------------- |
| `threshold`               | `FLOAT32` (PK) | Ngưỡng xác suất cắt $\tau \in [0.01, 0.99]$                                                          |
| `total_contacts`          | `INT32`        | Số lượng khách hàng được can thiệp tại ngưỡng này                                                    |
| `true_positives`          | `INT32`        | Số khách hàng mua được nhắm trúng                                                                    |
| `false_positives`         | `INT32`        | Số khách hàng không mua bị liên hệ nhầm (lãng phí chi phí)                                           |
| `expected_net_profit_usd` | `FLOAT32`      | Tổng lợi nhuận ròng mang lại tại ngưỡng                                                              |
| `precision`               | `FLOAT32`      | Độ chuẩn xác                                                                                         |
| `recall`                  | `FLOAT32`      | Tỷ lệ thâu tóm đơn hàng                                                                              |
| `f1_score`                | `FLOAT32`      | Điểm F1                                                                                              |
| `roi_percentage`          | `FLOAT32`      | Tỷ suất hoàn vốn tiếp thị: $\frac{\text{Lợi nhuận ròng}}{\text{Tổng chi phí tiếp thị}} \times 100\%$ |
