# .agy/00_CORE_RULES.md

## QUY CHUẨN KỸ THUẬT VÀ NGUYÊN TẮC BẤT BIẾN CHO AGENT (AGY)

Tài liệu này là hiến pháp vận hành bắt buộc cho AI Agent (`agy`) trong suốt quá trình lập trình, phân tích và xuất bản báo cáo. Mọi hành động vi phạm các quy tắc dưới đây đều bị coi là lỗi nghiêm trọng.

---

### 1. NGUYÊN TẮC TRUNG THỰC VÀ CHỐNG BỊA ĐẶT DỮ LIỆU (ZERO-FABRICATION RULE)

1. **Nghiêm cấm bịa đặt số liệu:** Tuyệt đối không tự ý điền trước, ước lượng, giả định hoặc chèn các giá trị metric (PR-AUC, ROC-AUC, F1-score, Precision, Recall, ECE, p-value, tỷ lệ phần trăm, v.v.) vào bất kỳ file code, cấu hình, bảng biểu hay báo cáo nào khi code chưa chạy thực tế.
2. **Khả năng truy xuất 100% (Traceability):** Mọi con số xuất hiện trên bảng biểu, báo cáo Word hay giao diện trực quan phải đọc trực tiếp từ các file kết quả thực nghiệm (`.json`, `.csv`, `.parquet`) do pipeline tính toán và lưu trong thư mục `outputs/`.
3. **Báo cáo trung thực:** Nếu dữ liệu không đủ để kiểm chứng một giả định hoặc kết quả mô hình không đạt kỳ vọng (ví dụ: metric giảm, p-value > 0.05), phải báo cáo đúng sự thật và phân tích hạn chế; nghiêm cấm can thiệp làm sai lệch kết quả.

---

### 2. NGUYÊN TẮC BẢO VỆ TÊN RIÊNG VÀ BẢO MẬT (PRIVACY & ANONYMITY)

1. **Cấm chèn tên cá nhân:** Tuyệt đối không đưa tên riêng của người dùng, tên sinh viên, mã số sinh viên, tên giảng viên, tên khoa hay tên trường vào mã nguồn Python, SQL, shell script, tên biến, tên hàm, chú thích (comment), file cấu hình YAML hay tài liệu kỹ thuật.
2. **Bảo mật cấu hình:** Các tham số hệ thống phải được đọc từ file cấu hình chung (`configs/base_config.yaml`), không hardcode các đường dẫn nhạy cảm mang tính cá nhân.

---

### 3. NGUYÊN TẮC BẢO TOÀN POINT-IN-TIME VÀ CÔ LẬP DỮ LIỆU (ANTI-LEAKAGE RULE)

1. **Ranh giới thời gian Point-in-Time (PIT):**
   - Thiết lập mốc chốt cutoff $t_0$. Toàn bộ đặc trưng lịch sử ($X$) chỉ được phép tính toán từ các sự kiện có mốc thời gian $\le t_0$.
   - Nhãn mục tiêu ($target \in \{0, 1\}$) chỉ được xác định từ hành vi giao dịch phát sinh trong cửa sổ tương lai $(t_0, t_0 + 30\text{ ngày}]$.
   - Tuyệt đối không sử dụng thông tin sau $t_0$ để tính toán đặc trưng (ngăn chặn hoàn toàn Future Data Leakage).
2. **Cô lập tập Holdout Test:**
   - Dữ liệu đánh giá cuối cùng (Holdout Test) phải được cô lập hoàn toàn khỏi quá trình xây dựng đặc trưng, điền giá trị thiếu (Imputation), chuẩn hóa (Scaling), mã hóa (Encoding), lựa chọn đặc trưng và tối ưu hóa siêu tham số (Optuna).
   - Mọi biến đổi dữ liệu có học tham số chỉ được phép thực hiện qua phương thức `fit()` trên tập Train; tập Holdout chỉ được áp dụng `transform()` duy nhất một lần ở bước đánh giá kiểm định cuối cùng.
3. **Kiểm tra loại trừ trường định danh:** Các trường `customer_id`, `session_id`, `transaction_id` và biến nhãn `target` tuyệt đối không được đưa vào ma trận đặc trưng đầu vào phục vụ huấn luyện mô hình.

---

### 4. NGUYÊN TẮC QUẢN TRỊ TÀI NGUYÊN PHẦN CỨNG (RESOURCE THROTTLING)

1. **Cấu hình máy đích:** CPU AMD Ryzen 5 3500U (4 nhân, 8 luồng), 16GB RAM.
2. **Giới hạn thực thi cho DuckDB:**
   - Luôn khởi tạo:
     ```sql
     SET threads = 6;
     SET max_memory = '10GB';
     ```
3. **Giới hạn thực thi cho Machine Learning:**
   - Các thuật toán (LightGBM, CatBoost, XGBoost, Scikit-learn) luôn thiết lập `n_jobs = 6` hoặc `thread_count = 6`.
   - Thuật toán Optuna: Giới hạn tối đa 30–35 trials; tích hợp `EarlyStoppingCallback` (dừng sau 7 trials liên tiếp không cải thiện PR-AUC).
4. **Kiểm soát bộ nhớ RAM:**
   - Tối ưu hóa kiểu dữ liệu dạng cột (`float32`, `int32`, `category`).
   - Sau mỗi công đoạn xử lý bảng dữ liệu lớn, phải giải phóng bộ nhớ tường minh bằng:
     ```python
     import gc
     gc.collect()
     ```

---

### 5. NGUYÊN TẮC CHUYỂN HÓA TỪ SỐ LIỆU SANG INSIGHT VÀ GIÁ TRỊ KINH DOANH

1. **Không dừng lại ở mô tả kỹ thuật:** Mỗi biểu đồ, bảng số liệu hoặc metric xuất ra bắt buộc phải trả lời được 3 câu hỏi:
   - _Phát hiện này phản ánh rào cản hành vi nào của khách hàng?_
   - _Bằng chứng định lượng nào chứng minh điều đó?_
   - _Doanh nghiệp cần thực hiện hành động tiếp thị/vận hành cụ thể nào để giải quyết?_
2. **Định lượng giá trị tiền tệ (Expected Profit Optimization):**
   - Không đánh giá mô hình bằng ngưỡng mặc định $\tau = 0.5$.
   - Bắt buộc lập phương trình hàm lợi nhuận kinh tế dựa trên giả định: Biên lợi nhuận gộp $= 25\%$ giá trị đơn hàng, Chi phí tiếp cận $C_{\text{contact}} = \$1.0$, Chi phí ưu đãi kích hoạt $C_{\text{voucher}} = \$5.0$.
   - Tìm kiếm ngưỡng quyết định tối ưu $\tau^*$ mang lại lợi nhuận ròng cực đại.
3. **Bắt buộc cho Phân tích & Đề xuất (Đặc biệt ở Giai đoạn 5 / Phần 5):**
   - Mọi phân khúc khách hàng (GMM), nhóm phản ứng (Uplift) và phân vị (Decile Lift@K) phải gắn liền với chân dung kinh doanh cụ thể.
   - Các đề xuất kinh doanh phải nêu rõ: Đối tượng mục tiêu, Hành động đề xuất, Kênh can thiệp, Ngưỡng can thiệp, Rủi ro đi kèm và KPI đo lường (ROI, Conversion Lift).

---

### 6. QUY CHUẨN THIẾT KẾ ĐỒ HỌA HỌC THUẬT (VISUAL STANDARDS)

1. **Bảng màu tinh giản (Tri-Color Palette):**
   - Màu nền đồ thị: `#F8FAFC` (Slate Off-white).
   - Màu chủ đạo / Khối dữ liệu chính: `#0F172A` (Midnight Navy).
   - Màu nhấn tích cực (Chuyển đổi, Lợi nhuận, Thành công): `#0D9488` (Forest Emerald).
   - Màu nhấn cảnh báo (Rào cản, Bỏ giỏ hàng, Rời bỏ, Lỗ): `#E11D48` (Crimson Coral).
   - Tuyệt đối không dùng bảng màu cầu vồng mặc định (Jet, Rainbow) gây rối mắt.
2. **Quy chuẩn bố cục:**
   - Font chữ: Sans-serif (Roboto, Inter hoặc Arial).
   - Luôn loại bỏ khung viền trên và phải (`sns.despine()`).
   - Lưới phụ (Grid) màu xám mờ (`#E2E8F0`) với độ mờ `alpha = 0.3`.
   - Có tiêu đề chính (Title) nêu bật insight và phụ đề (Subtitle) nêu rõ phạm vi dữ liệu.
   - Thêm chú thích trực tiếp (Annotation / Callout) vào điểm uốn, mốc thời gian hoặc ngưỡng tối ưu thay vì để người đọc tự dò toạ độ.
3. **Xuất file:** Mọi biểu đồ lưu dưới định dạng `.png` với độ phân giải `dpi = 300` tại thư mục `outputs/figures/`.

---

### 7. QUẢN LÝ THỰC NGHIỆM VÀ KHẢ NĂNG TÁI LẬP (EXPERIMENT GOVERNANCE)

1. **Lưu vết bất biến (Append-Only):**
   - Mỗi lần chạy thí nghiệm mô hình phải khởi tạo thư mục riêng: `outputs/experiments/EXP_<tên_mô_hình>_<timestamp>/`.
   - Lưu trữ đầy đủ: `config.yaml`, `data_hash.json` (SHA-256 hash của dữ liệu đầu vào), `run.log`, `metrics.json`.
   - Tuyệt đối không ghi đè hoặc xóa các kết quả thí nghiệm đã chạy trước đó.
2. **Kiểm thử tự động trước khi xuất báo cáo (`tests/`):**
   - Phải chạy và pass 100% các bài kiểm tra:
     - `test_disjoint_split`: Không có khách hàng nào trùng lặp giữa Train và Holdout.
     - `test_no_future_leakage`: Đặc trưng không thay đổi khi thêm sự kiện sau $t_0$.
     - `test_probability_validity`: Xác suất dự đoán nằm đúng trong đoạn $[0, 1]$, không chứa giá trị `NaN` hoặc `Inf`.
