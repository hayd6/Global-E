# PHÂN TÍCH RÀO CẢN CHUYỂN ĐỔI GIỎ HÀNG VÀ TỐI ƯU HÓA LỢI NHUẬN TIẾP THỊ TRONG THƯƠNG MẠI ĐIỆN TỬ

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database Engine](https://img.shields.io/badge/engine-DuckDB%20%2B%20Parquet-orange.svg)](https://duckdb.org/)
[![Framework](https://img.shields.io/badge/framework-FastAPI%20%2B%20Next.js%2014-black.svg)](https://nextjs.org/)
[![BI Dashboard](https://img.shields.io/badge/BI-Microsoft%20Power%20BI%20PBIP-yellow.svg)](https://powerbi.microsoft.com/)
[![Web Deployment](https://img.shields.io/badge/portal-GitHub%20Pages%20Live-success.svg)](https://hayd6.github.io/Global-E/)

> **ĐỒ ÁN CUỐI KỲ | HỌC KỲ 1 – ĐỢT 1 – NĂM HỌC 2026-2027**  
> **Môn học:** Ứng dụng phân tích dữ liệu lớn trong kinh doanh (Big Data)  
> **Mã lớp học phần:** `ABDA433708_02`  
> **Đơn vị:** Khoa Kinh Tế – Trường Đại học Công nghệ Kỹ thuật TP. Hồ Chí Minh  
> **Giảng viên hướng dẫn:** ThS. Nguyễn Phan Anh Huy  
> **Nhóm thực hiện:** Nhóm 9  
> **File báo cáo Word chính thức:** [`ABDA433708_02_Nhom9_CuoiKi.docx`](./ABDA433708_02_Nhom9_CuoiKi.docx)  
> **Cổng thông tin ra quyết định trực tuyến (Live Portal):** [https://hayd6.github.io/Global-E/](https://hayd6.github.io/Global-E/)

---

## Giới thiệu tổng quan đề tài

Dự án nghiên cứu và xây dựng **Khung phân tích dữ liệu lớn hỗ trợ ra quyết định kinh tế (Prescriptive Decision Intelligence Framework)** trong thương mại điện tử. Hệ thống kết nối xuyên suốt từ kỹ thuật dữ liệu lớn bảo toàn tính bất biến thời gian (Point-in-Time), mô hình hóa rào cản hành vi vi mô và phân cụm xác suất GMM, dự đoán xu hướng chuyển đổi hiệu chỉnh (Calibrated Propensity), định lượng thời gian sống còn giỏ hàng (Survival Analysis), suy luận nhân quả tiếp thị (Uplift Modeling T-Learner CATE), đến tối ưu hóa hàm lợi nhuận ròng What-If.

---

## 1. Cấu trúc thư mục dự án chuẩn hóa

Dự án được tổ chức theo chuẩn kỹ thuật phần mềm và khoa học dữ liệu hiện đại, tinh gọn và minh bạch:

```text
global-ecommerce-decision-intelligence/
├── ABDA433708_02_Nhom9_CuoiKi.docx     # Báo cáo khoa học chính thức của đồ án (Word)
├── configs/
│   ├── base_config.yaml                 # Cấu hình trung tâm (đường dẫn, phần cứng, tham số tài chính)
│   └── experiments/                     # Checkpoint tham số thực nghiệm
├── data/
│   ├── raw/                             # Thư mục chứa 8 file CSV thô (tải về từ Kaggle)
│   └── processed/                       # Feature Store chuẩn Point-in-Time (.parquet)
├── src/
│   ├── data_engineering/                # DuckDB xử lý dữ liệu phục hồi (Healing) & PIT Feature Store
│   ├── analytics/                       # Kiểm định phi tham số & Phân cụm GMM (k*=5) & Survival Analysis
│   ├── models/                          # Huấn luyện mô hình (CatBoost, LightGBM, XGBoost, Stacking), Uplift
│   ├── explainability/                  # TreeSHAP & ma trận tương tác cặp biến
│   ├── business_value/                  # Tối ưu hóa lợi nhuận kỳ vọng What-If & Ma trận hành động
│   ├── utils/                           # Điều phối báo cáo tự động và tiện ích logging
│   └── visualization/                   # Script sinh cấu trúc Star-Schema cho Power BI PBIR
├── tests/                               # Kiểm thử tự động tính toàn vẹn PIT (Zero-leakage)
├── outputs/
│   ├── figures/                         # Toàn bộ biểu đồ khoa học chuẩn xuất bản (300 DPI, Tri-Color)
│   ├── tables/                          # 18 bảng số liệu thực nghiệm trích xuất tự động (.csv)
│   ├── models/                          # File nhị phân lưu mô hình tốt nhất (.pkl)
│   ├── experiments/                     # Nhật ký thực thi pipeline (pipeline_run.log)
│   └── powerbi/                         # Dự án Power BI Project (.pbip) và Star-Schema sạch 4 trang
├── api/                                 # FastAPI Backend (Port 8000) phục vụ suy luận mô hình
│   └── main.py
├── web/                                 # Cổng thông tin tương tác Next.js 14 App Router & Tailwind CSS
│   ├── src/app/                         # Giao diện 6 phần tích hợp Executive Dashboard & 3D WebGL
│   └── public/
├── app/                                 # Ứng dụng Web tương tác Streamlit (nghiệm thu nội bộ)
│   └── app.py
├── requirements.txt                     # Danh mục thư viện Python bắt buộc
└── run_pipeline.py                      # Kịch bản thực thi tự động toàn diện (1-Click Execution)
```

---

## 2. Hướng dẫn nạp dữ liệu thô (`data/raw/`)

> [!IMPORTANT]
> **LƯU Ý VỀ DỮ LIỆU THÔ:**  
> Do bộ dữ liệu gốc có dung lượng lớn (>100 MB với hơn 200.000 hồ sơ khách hàng, 2.000.000 phiên truy cập và 500.000 giao dịch), các file CSV thô **không được đẩy lên GitHub** theo quy tắc `.gitignore` để tránh tràn bộ nhớ repository.

Để chạy lại pipeline dữ liệu từ đầu, vui lòng thực hiện tải bộ dữ liệu theo hướng dẫn:

1. **Nguồn dữ liệu:** Cuộc thi / Bộ dữ liệu trên Kaggle:  
   👉 **[Global E-Commerce Customer Purchase Prediction Dataset](https://www.kaggle.com/competitions/global-e-commerce-customer-purchase-prediction/data)**
2. Tải về và giải nén toàn bộ **8 file CSV** đặt trực tiếp vào thư mục `data/raw/`:
   * `customers.csv` (Hồ sơ khách hàng)
   * `sessions.csv` (Lịch sử phiên truy cập)
   * `transactions.csv` (Lịch sử giao dịch đơn hàng)
   * `marketing_campaigns.csv` (Chiến dịch tiếp thị)
   * `geo_data.csv` (Dữ liệu địa lý vùng miền)
   * `train.csv` (Tập train gốc)
   * `test.csv` (Tập test gốc)
   * `sample_submission.csv` (File mẫu nộp bài)

---

## 3. Hướng dẫn cài đặt & Thực thi dự án (1-Click Pipeline)

Quy trình dưới đây áp dụng như nhau cho cả trường hợp **Clone từ GitHub** hoặc **Giải nén từ file nộp `.zip`**:

### Bước 1: Mở Terminal tại thư mục gốc của dự án
* Nếu sử dụng Git:
  ```bash
  git clone https://github.com/hayd6/Global-E.git
  cd Global-E
  ```
* Nếu giải nén từ file `.zip`: Mở PowerShell / Command Prompt tại thư mục vừa giải nén.

### Bước 2: Khởi tạo môi trường ảo và cài đặt thư viện
Khuyến nghị sử dụng **Python 3.10+**:
```bash
# Tạo môi trường ảo (khuyến nghị)
python -m venv venv

# Kích hoạt môi trường ảo:
# Trên Windows:
.\venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt toàn bộ thư viện bắt buộc
pip install -r requirements.txt
```

### Bước 3: Chạy kiểm thử tự động tính toàn vẹn Point-in-Time (PIT Integrity Test)
Xác thực nguyên tắc nghiêm ngặt: $100\%$ không rò rỉ dữ liệu qua mốc chốt quyết định $t_0 = \text{2024-06-01}$:
```bash
pytest tests/test_pit_integrity.py -v
```

### Bước 4: Thực thi trọn vẹn toàn bộ Pipeline từ A đến Z (1-Click Run)
```bash
python run_pipeline.py
```
*Script tự động điều phối tuần tự 18 công đoạn qua 5 giai đoạn: Data Healing bằng DuckDB $\rightarrow$ Feature Store PIT $\rightarrow$ Kiểm định giả thuyết & GMM $\rightarrow$ Optuna Tuning & Calibration $\rightarrow$ Kaplan-Meier, CoxPH & Uplift CATE $\rightarrow$ Tối ưu hóa lợi nhuận What-If $\rightarrow$ Xuất bản Star-Schema Power BI.*

---

## 4. Hướng dẫn trải nghiệm các nền tảng Dashboard & Ứng dụng

Dự án cung cấp 4 kênh nghiệm thu trực quan phục vụ người dùng nghiệp vụ và ban điều hành:

### 4.1. Cổng thông tin điều hành trực tuyến (Web Portal - Khuyến nghị)
* **Truy cập trực tiếp không cần cài đặt:**  
  👉 **[https://hayd6.github.io/Global-E/](https://hayd6.github.io/Global-E/)**
* Hoặc chạy cục bộ bằng Node.js:
  ```bash
  cd web
  npm install
  npm run dev
  ```
  Truy cập tại: `http://localhost:3000`

### 4.2. Báo cáo quản trị thông minh Microsoft Power BI (4 trang chuyên sâu)
* Mở trực tiếp bằng phần mềm **Microsoft Power BI Desktop**:
  * File dự án mã nguồn mở: [`outputs/powerbi/dashboards.pbip`](./outputs/powerbi/dashboards.pbip)
  * Hoặc file đóng gói: [`outputs/powerbi/dashboards.pbix`](./outputs/powerbi/dashboards.pbix)
* **Cấu trúc 4 trang dashboard:**
  1. *Trang 1:* Tổng quan điều hành & Động học phễu chuyển đổi (Baymard vs Global-E, CVR theo độ tuổi & quốc gia).
  2. *Trang 2:* Rào cản hành vi vi mô & Phân cụm xác suất GMM ($k^*=5$ chân dung khách hàng).
  3. *Trang 3:* Động học sống còn Kaplan-Meier & Suy luận nhân quả Uplift CATE.
  4. *Trang 4:* Tối ưu hóa hàm lợi nhuận ròng What-If ($\tau^* = 0.07$) & Ma trận hành động kinh doanh.

### 4.3. Backend API suy luận mô hình (FastAPI)
Cung cấp API phục vụ dự báo xác suất chuyển đổi, giải thích SHAP và tính toán phân khúc thời gian thực:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
*Tài liệu kiểm thử tương tác Swagger UI:* `http://localhost:8000/docs`

### 4.4. Ứng dụng Web tương tác Streamlit
```bash
streamlit run app/app.py
```
*Truy cập tại:* `http://localhost:8501`

---

## 5. Danh mục sản phẩm bàn giao đồ án (Deliverables)

1. **Báo cáo khoa học Word chuyên sâu:** File [`ABDA433708_02_Nhom9_CuoiKi.docx`](./ABDA433708_02_Nhom9_CuoiKi.docx) chuẩn cấu trúc học thuật, tích hợp đầy đủ cơ sở lý thuyết, công thức toán học, bảng số liệu thực nghiệm và đánh giá giá trị kinh tế.
2. **Cổng thông tin ra quyết định số (Web Portal):** Phát hành trên GitHub Pages tại [hayd6.github.io/Global-E](https://hayd6.github.io/Global-E/) tích hợp đồ thị 3D WebGL và mô phỏng What-If thời gian thực.
3. **Bộ Dashboard Power BI Star-Schema hoàn chỉnh:** [`outputs/powerbi/`](./outputs/powerbi/) gồm 4 bảng thứ nguyên và 1 bảng sự kiện kết nối mô hình quan hệ chuẩn 1-N.
4. **Mô hình học máy tối ưu sẵn sàng triển khai:** `outputs/models/best_calibrated_model.pkl` (LightGBM kết hợp Platt Sigmoid Calibration, nén ECE xuống 0.0035).
5. **Kho lưu trữ số liệu & biểu đồ khoa học:** 18 bảng số liệu tại `outputs/tables/` và 12 biểu đồ độ phân giải cao tại `outputs/figures/`.
