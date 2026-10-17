# .agy/03_PROPENSITY_AND_CALIBRATION.md

## GIAI ĐOẠN 3: HUẤN LUYỆN MÔ HÌNH DỰ ĐOÁN CHUYỂN ĐỔI SOTA, TỐI ƯU HÓA SIÊU THAM SỐ OPTUNA VÀ HIỆU CHỈNH XÁC SUẤT

### 1. QUY TẮC BẮT BUỘC KHI THỰC THI CHO AGENT (AGY)

1. **Tự động hóa hoàn toàn:** Agent (`agy`) đọc tài liệu này, tự khởi tạo các module mã nguồn Python, tự thực thi bằng môi trường cục bộ và tự động kiểm tra tính hợp lệ của các file kết quả (`.csv`, `.json`, `.png`, `.pkl`). Tuyệt đối không yêu cầu người dùng thao tác thủ công.
2. **Quy tắc bảo mật & danh tính:** Không đưa tên riêng, thông tin cá nhân hay bất kỳ định danh nào vào mã nguồn, chú thích (comment) hay tên tệp. Cố định `random_state = 42`.
3. **Trung thực số liệu (Zero-Fabrication):** Mọi chỉ số đánh giá (PR-AUC, ROC-AUC, F1-score, Brier score, ECE, runtime) bắt buộc phải tính toán trực tiếp từ dữ liệu thực nghiệm trên tập Holdout Test. Nghiêm cấm gán cứng giá trị giả định.
4. **Quản trị tài nguyên phần cứng (Ryzen 5 3500U, 16GB RAM):**
   - Thiết lập `n_jobs = 6` hoặc `thread_count = 6` cho tất cả các mô hình và Optuna.
   - Giới hạn Optuna ở mức 30–35 trials/mô hình, tích hợp `EarlyStoppingCallback` (dừng sau 7 trials liên tiếp không cải thiện PR-AUC).
   - Giải phóng RAM bằng `import gc; gc.collect()` sau mỗi vòng lặp Cross-Validation và sau khi huấn luyện xong mỗi họ mô hình.

---

### 2. CÁC TÁC VỤ LẬP TRÌNH VÀ THỰC THI CHI TIẾT

#### Tác vụ 3.1: Module phân chia dữ liệu và huấn luyện mô hình cơ sở (`src/models/train_propensity_models.py`)

`agy` có nhiệm vụ tạo file `src/models/train_propensity_models.py` và chạy script với các yêu cầu:

1. **Phân chia dữ liệu phân tầng và lưu trữ chỉ số:**
   - Đọc bảng đặc trưng: `data/processed/customer_features_pit.parquet`.
   - Tách tập dữ liệu có nhãn (`train.csv` ban đầu gồm 160.000 dòng) thành:
     - Train Pool: 80% (128.000 dòng).
     - Holdout Test: 20% (32.000 dòng, hoàn toàn độc lập, chỉ dùng đánh giá cuối cùng).
   - Sử dụng `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
   - Lưu chỉ số phân chia ra file: `outputs/experiments/split_indices.npz` để đảm bảo khả năng tái lập 100%.
2. **Huấn luyện mô hình cơ sở (Baselines):**
   - _Logistic Regression:_ Đi kèm pipeline `StandardScaler()` và `SimpleImputer(strategy='median')`.
   - _Random Forest:_ Thiết lập `n_estimators = 200, max_depth = 12, min_samples_split = 20, n_jobs = 6, random_state = 42`.
   - Đánh giá trên Holdout Test (ngưỡng 0.5), ghi nhận thời gian huấn luyện (`fit_time`) và thời gian suy luận (`inference_time`).
3. **Tối ưu hóa siêu tham số mô hình SOTA bằng Optuna:**
   - Thực hiện 5-Fold Stratified Cross-Validation trên tập Train Pool. Hàm mục tiêu (Objective Function): Tối đa hóa trung bình PR-AUC trên 5 folds.
   - Không gian tìm kiếm (Search Spaces):
     - **LightGBM (`LGBMClassifier`):**
       - `learning_rate`: log-uniform $[0.01, 0.15]$
       - `num_leaves`: int $[15, 127]$
       - `max_depth`: int $[4, 10]$
       - `min_child_samples`: int $[20, 200]$
       - `subsample`: uniform $[0.6, 1.0]$
       - `colsample_bytree`: uniform $[0.6, 1.0]$
       - `scale_pos_weight`: uniform $[1.0, 5.0]$
     - **CatBoost (`CatBoostClassifier`):**
       - `learning_rate`: log-uniform $[0.01, 0.15]$
       - `depth`: int $[4, 9]$
       - `l2_leaf_reg`: int $[1, 10]$
       - `random_strength`: uniform $[0.1, 10.0]$
       - `auto_class_weights`: `Balanced`
     - **XGBoost (`XGBClassifier`):**
       - `learning_rate`: log-uniform $[0.01, 0.15]$
       - `max_depth`: int $[4, 9]$
       - `min_child_weight`: int $[1, 10]$
       - `subsample`: uniform $[0.6, 1.0]$
       - `colsample_bytree`: uniform $[0.6, 1.0]$
       - `scale_pos_weight`: uniform $[1.0, 5.0]$
   - Số lượng thử nghiệm: 35 trials/mô hình, dừng sớm sau 7 trials không tiến bộ.
   - Xuất bảng siêu tham số tối ưu ra: `outputs/tables/tbl_ch4_optuna_best_hyperparameters.csv`.
4. **Mô hình tổ hợp xếp chồng (Stacking Ensemble):**
   - Trích xuất dự đoán xác suất ngoài mẫu (Out-of-Fold predicted probabilities) từ 3 mô hình tốt nhất (CatBoost, LightGBM, Random Forest).
   - Huấn luyện mô hình siêu học (Meta-Learner): `LogisticRegression()` trên ma trận xác suất OOF.
   - Đánh giá mô hình Stacking trên tập Holdout Test.

---

#### Tác vụ 3.2: Module hiệu chỉnh xác suất và đánh giá toàn diện (`src/models/calibrate_and_evaluate.py`)

`agy` có nhiệm vụ tạo file `src/models/calibrate_and_evaluate.py` và chạy script với các yêu cầu:

1. **Hiệu chỉnh xác suất thực nghiệm (Probability Calibration):**
   - Sử dụng `CalibratedClassifierCV(cv='prefit')` trên mô hình LightGBM và CatBoost tốt nhất.
   - So sánh 2 phương pháp: `method='isotonic'` (phi tham số) và `method='sigmoid'` (Platt Scaling).
   - Đo lường mức độ tin cậy bằng Brier Score và Expected Calibration Error (ECE với $M = 10$ bins).
   - Lưu trữ mô hình hiệu chỉnh tốt nhất phục vụ ứng dụng thực tế ra file:
     `outputs/models/best_calibrated_model.pkl`.
2. **Xuất bảng so sánh tổng thể các mô hình:**
   - Đánh giá tất cả các mô hình trên tập Holdout Test (32.000 mẫu Unseen).
   - Tính toán đầy đủ các chỉ số: `PR-AUC`, `ROC-AUC`, `F1-score`, `Precision`, `Recall`, `Accuracy`, `Brier_Score`, `ECE`, `Fit_Time_Sec`, `Inference_Latency_MS`.
   - Xuất bảng ra file: `outputs/tables/tbl_ch4_model_benchmark_comparison.csv`.

---

#### Tác vụ 3.3: Module thực nghiệm chiều sâu: Ablation Study và kiểm định đa hạt giống (`src/models/ablation_and_stability.py`)

`agy` có nhiệm vụ tạo file `src/models/ablation_and_stability.py` và chạy script với các yêu cầu:

1. **Ablation Study (Đo lường giá trị thông tin của từng nhóm biến):**
   - Sử dụng mô hình LightGBM tối ưu, huấn luyện và đánh giá trên 4 cấu hình đặc trưng:
     - Cấu hình 1: Full Features (Toàn bộ đặc trưng).
     - Cấu hình 2: Loại bỏ nhóm đặc trưng rào cản giỏ hàng (`cart_*`).
     - Cấu hình 3: Loại bỏ nhóm đặc trưng giao dịch lịch sử (`trans_*`, `spend_*`).
     - Cấu hình 4: Loại bỏ nhóm đặc trưng nhân khẩu & bối cảnh (`age`, `tier`, `geo_*`).
   - Ghi nhận mức suy giảm của PR-AUC và F1-score để chứng minh vai trò quyết định của nhóm đặc trưng rào cản giỏ hàng.
   - Xuất kết quả ra file: `outputs/tables/tbl_ch4_ablation_study_results.csv`.
2. **Kiểm định độ ổn định qua 5 hạt giống ngẫu nhiên (Multi-Seed Testing):**
   - Chạy mô hình LightGBM tốt nhất trên 5 seeds độc lập: `[42, 100, 2024, 2026, 777]`.
   - Tính giá trị trung bình (Mean) và độ lệch chuẩn (Std) của PR-AUC, ROC-AUC, Brier Score.
   - Xuất kết quả ra file: `outputs/tables/tbl_ch4_multiseed_stability.csv`.

---

#### Tác vụ 3.4: Module xuất biểu đồ đánh giá chuẩn xuất bản 300 DPI (`src/models/plot_model_evaluation.py`)

`agy` có nhiệm vụ tạo file `src/models/plot_model_evaluation.py` và chạy script để kết xuất hình ảnh:

- Quy chuẩn thẩm mỹ: Nền `#F8FAFC`, Khối chính `#0F172A`, Nhấn tích cực `#0D9488`, Nhấn rào cản `#E11D48`, độ phân giải 300 DPI, font chữ sans-serif, despine viền trên/phải, lưới mờ `alpha = 0.3`.
  Nội dung 3 biểu đồ cần xuất:

1. `outputs/figures/fig_ch4_01_roc_pr_curves_comparison.png`:
   - Đồ thị đôi: Bên trái là ROC Curves, bên phải là Precision-Recall Curves của 6 mô hình chính.
   - Hiển thị rõ giá trị diện tích dưới đường cong (AUC) ngay trong khung chú giải (Legend).
2. `outputs/figures/fig_ch4_02_calibration_curves.png`:
   - Biểu đồ đường cong hiệu chỉnh xác suất (Reliability Diagram) so sánh trước và sau khi áp dụng Isotonic/Sigmoid Calibration so với đường chuẩn hoàn hảo 45 độ.
   - Biểu đồ cột phụ bên dưới thể hiện tần suất phân phối xác suất dự đoán.
3. `outputs/figures/fig_ch4_03_ablation_study_bar.png`:
   - Biểu đồ cột ngang thể hiện mức suy giảm PR-AUC khi loại bỏ tuần tự từng nhóm đặc trưng, có chú thích trực tiếp phần trăm suy giảm (%) trên từng thanh.

---

### 3. QUY TRÌNH THỰC THI TỰ ĐỘNG CHO AGENT

Khi kích hoạt giai đoạn 3, `agy` tự động chạy tuần tự các lệnh sau trong terminal, tự kiểm tra mã lỗi và hoàn tất toàn bộ pipeline:

```bash
python src/models/train_propensity_models.py
python src/models/calibrate_and_evaluate.py
python src/models/ablation_and_stability.py
python src/models/plot_model_evaluation.py

4. TIÊU CHÍ NGHIỆM THU HOÀN THÀNH (DEFINITION OF DONE)
Giai đoạn 3 được coi là hoàn tất khi:

[ ] Tệp outputs/experiments/split_indices.npz được tạo đầy đủ.

[ ] Tệp outputs/tables/tbl_ch4_optuna_best_hyperparameters.csv ghi nhận đầy đủ tham số tối ưu của 3 họ mô hình Boosting.

[ ] Tệp outputs/models/best_calibrated_model.pkl được xuất thành công, có khả năng gọi hàm .predict_proba() trả về xác suất chuẩn.

[ ] Tệp outputs/tables/tbl_ch4_model_benchmark_comparison.csv ghi nhận đầy đủ 10 chỉ số cho tất cả các mô hình trên tập Holdout Test 32.000 dòng.

[ ] Tệp outputs/tables/tbl_ch4_ablation_study_results.csv và outputs/tables/tbl_ch4_multiseed_stability.csv được tạo đầy đủ số liệu tính toán thực tế.

[ ] Ba tệp ảnh fig_ch4_01_roc_pr_curves_comparison.png, fig_ch4_02_calibration_curves.png và fig_ch4_03_ablation_study_bar.png nằm trong outputs/figures/, đạt chuẩn 300 DPI và tuân thủ bảng màu quy định.
```
