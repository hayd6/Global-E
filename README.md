# Phân tích rào cản chuyển đổi giỏ hàng và tối ưu hóa lợi nhuận tiếp thị trong thương mại điện tử

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/engine-DuckDB%20%2B%20Parquet-orange.svg)](https://duckdb.org/)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

Hệ thống nghiên cứu phân tích dữ liệu lớn và hỗ trợ ra quyết định kinh tế (Prescriptive Decision Framework) cho thương mại điện tử. Dự án tập trung giải mã các điểm gãy trong phễu giỏ hàng, phân khúc hành vi đa chiều, dự đoán xác suất chuyển đổi được hiệu chỉnh (Calibrated Propensity), định lượng thời gian phân rã giỏ hàng (Survival Analysis), phân bổ can thiệp tiếp thị nhân quả (Uplift Modeling) và tối ưu hóa lợi nhuận kỳ vọng (Expected Profit Optimization).

---

## 1. Cấu trúc thư mục dự án

```text
global-ecommerce-decision-intelligence/
├── .agy/                                # Chỉ dẫn thực thi cho Antigravity (agy)
│   ├── 00_CORE_RULES.md                 # Quy chuẩn trung thực, chống rò rỉ PIT, bảo vệ tên riêng
│   ├── 01_DATA_ENGINEERING_PIT.md       # Lệnh DuckDB, data healing & feature store PIT
│   ├── 02_BEHAVIORAL_SEGMENTATION.md    # Lệnh EDA rào cản giỏ hàng & phân khúc GMM/HDBSCAN
│   ├── 03_PROPENSITY_AND_CALIBRATION.md # Lệnh CatBoost/LGBM/XGBoost + Optuna + Calibration
│   ├── 04_SURVIVAL_UPLIFT_OPTIMIZATION.md # Lệnh Survival, Uplift Modeling & tối ưu hóa lợi nhuận
│   └── 05_DASHBOARD_WEB_AND_REPORT.md   # Lệnh xuất Star-Schema Power BI, Web App & Báo cáo
├── configs/
│   ├── base_config.yaml                 # Cấu hình trung tâm (đường dẫn, tài nguyên, giả định)
│   └── experiments/                     # Checkpoint cấu hình cho từng lượt chạy
├── data/
│   ├── raw/                             # 8 file CSV gốc từ Kaggle
│   └── processed/                       # Bảng Feature Store chuẩn Point-in-Time (.parquet)
├── src/
│   ├── data_engineering/                # Script DuckDB làm sạch và trích xuất đặc trưng
│   ├── analytics/                       # Phân khúc GMM/HDBSCAN & kiểm định giả thuyết
│   ├── models/                          # Huấn luyện mô hình, Optuna, hiệu chỉnh xác suất, Uplift
│   ├── explainability/                  # TreeSHAP & ma trận tương tác cặp biến
│   ├── business_value/                  # Tối ưu hóa lợi nhuận kỳ vọng & tính toán Lift@K
│   └── utils/                           # Quản lý logging, tracking mã băm SHA-256
├── tests/                               # Kiểm thử tự động (Zero-leakage, Disjoint split)
├── outputs/
│   ├── experiments/                     # Lưu vết thực nghiệm độc lập theo từng lượt chạy
│   ├── figures/                         # Biểu đồ chuẩn xuất bản (300 DPI, Tri-Color Palette)
│   ├── tables/                          # Toàn bộ bảng số liệu trích xuất tự động (.csv)
│   ├── models/                          # File nhị phân lưu mô hình tốt nhất (.pkl)
│   └── powerbi/                         # 4 file Star-Schema sạch phục vụ nạp Power BI
├── app/                                 # Ứng dụng Web tương tác Streamlit kết nối mô hình thật
├── docs/                                # Báo cáo nghiên cứu Word, Slide và kịch bản video
├── PRD.md                               # Bản đặc tả yêu cầu dự án
├── requirements.txt                     # Danh mục thư viện Python bắt buộc
└── run_pipeline.py                      # Kịch bản thực thi tự động toàn diện (1-Click Run)
```

---

## 2. Hướng dẫn thực thi toàn diện (1-Click Execution)

### Bước 1: Kích hoạt môi trường và cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy kiểm thử tự động tính toàn vẹn Point-in-Time (PIT)
```bash
pytest tests/test_pit_integrity.py -v
```

### Bước 3: Thực thi trọn vẹn Pipeline từ A đến Z (1-Click Pipeline)
```bash
python run_pipeline.py
```
*Lưu ý: Script điều phối tuần tự 18 công đoạn qua 5 giai đoạn, tự động kiểm tra RAM, logging và đồng bộ hóa artifacts.*

---

## 3. Khởi chạy Ứng dụng Web Ra Quyết định Streamlit
Ứng dụng tương tác 3 tabs (`Customer Diagnostic`, `What-If Profit Simulator`, `Uplift Strategy Matrix`) kết nối trực tiếp mô hình hiệu chỉnh nhị phân:
```bash
streamlit run app/app.py
```

---

## 4. Danh mục sản phẩm bàn giao chính (Key Deliverables)
1. **Báo cáo nghiên cứu khoa học chuyên sâu:** `docs/BaoCao_CuoiKy_ChiTiet.docx` (6 chương, chuẩn học thuật APA, bảng biểu và biểu đồ trích xuất tự động từ dữ liệu thực).
2. **Kịch bản thuyết trình & Slide Deck:** `docs/SLIDE_OUTLINE.md` (18 slides chi tiết) và `docs/VIDEO_SCRIPT.md` (3-5 phút).
3. **Mô hình triển khai sản xuất:** `outputs/models/best_calibrated_model.pkl` (Pipeline hoàn chỉnh kết hợp Imputer + Calibrated Classifier).
4. **Bộ dữ liệu Power BI Star-Schema:** `outputs/powerbi/` (4 bảng quan hệ 1-N sẵn sàng import trực tiếp vào Power BI Desktop).
5. **Hệ thống bảng số liệu và biểu đồ:** 18 bảng CSV tại `outputs/tables/` và 12 biểu đồ 300 DPI Tri-Color Palette tại `outputs/figures/`.
