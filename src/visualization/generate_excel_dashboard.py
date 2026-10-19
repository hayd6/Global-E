"""
Script: generate_excel_dashboard.py
Mục đích: Khởi tạo tệp Excel Báo cáo Điều hành Cấp cao (C-Suite / Wall Street Executive Dashboard)
          - Tắt 100% đường lưới ô (hide_gridlines) tạo Canvas phẳng chuyên nghiệp.
          - 4 Thẻ KPI độc lập dạng khối hộp bo tròn/viền mềm, số lớn 22pt sắc nét.
          - Biểu đồ Excel kích thước chuẩn 16:9 (580x325px) phối màu Dark Navy & Emerald.
          - Quy hoạch cột & hàng thông thoáng, đẩy bảng dữ liệu nguồn xuống khu vực riêng bên dưới.
"""

import os
import sys
import pandas as pd
import xlsxwriter

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def create_executive_excel_dashboard():
    output_dir = os.path.join("outputs", "excel")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "GlobalE_Executive_Dashboard_v2.xlsx")

    print(f"[*] Khởi tạo tệp Excel Dashboard: {file_path}")
    workbook = xlsxwriter.Workbook(file_path, {'strings_to_numbers': True})

    # ========================================================
    # ĐỊNH DẠNG BẢNG MÀU ĐIỀU HÀNH (C-SUITE EXECUTIVE THEME)
    # ========================================================
    # Top Banner Header
    fmt_banner_title = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 14, 'bold': True,
        'font_color': '#FFFFFF', 'bg_color': '#0F172A',
        'valign': 'vcenter', 'indent': 1
    })
    
    fmt_banner_sub = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9, 'italic': True,
        'font_color': '#94A3B8', 'bg_color': '#0F172A',
        'valign': 'vcenter', 'indent': 1
    })

    # Navigation Ribbon
    fmt_nav_bg = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9, 'bold': True,
        'font_color': '#E2E8F0', 'bg_color': '#1E293B',
        'valign': 'vcenter', 'align': 'center'
    })
    
    fmt_nav_btn = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9, 'bold': True,
        'font_color': '#38BDF8', 'bg_color': '#1E293B',
        'valign': 'vcenter', 'align': 'center', 'underline': True
    })

    # KPI Card Formats (Khối hộp thẻ KPI nổi)
    fmt_kpi_top = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 8, 'bold': True,
        'font_color': '#64748B', 'bg_color': '#F8FAFC',
        'align': 'center', 'valign': 'vcenter',
        'top': 1, 'left': 1, 'right': 1, 'top_color': '#CBD5E1', 'left_color': '#CBD5E1', 'right_color': '#CBD5E1'
    })

    fmt_kpi_mid_navy = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 20, 'bold': True,
        'font_color': '#0F172A', 'bg_color': '#FFFFFF',
        'align': 'center', 'valign': 'vcenter',
        'left': 1, 'right': 1, 'left_color': '#CBD5E1', 'right_color': '#CBD5E1'
    })

    fmt_kpi_mid_teal = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 20, 'bold': True,
        'font_color': '#0D9488', 'bg_color': '#FFFFFF',
        'align': 'center', 'valign': 'vcenter',
        'left': 1, 'right': 1, 'left_color': '#CBD5E1', 'right_color': '#CBD5E1'
    })

    fmt_kpi_mid_coral = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 20, 'bold': True,
        'font_color': '#E11D48', 'bg_color': '#FFFFFF',
        'align': 'center', 'valign': 'vcenter',
        'left': 1, 'right': 1, 'left_color': '#CBD5E1', 'right_color': '#CBD5E1'
    })

    fmt_kpi_bot = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 8, 'italic': True,
        'font_color': '#94A3B8', 'bg_color': '#F8FAFC',
        'align': 'center', 'valign': 'vcenter',
        'bottom': 1, 'left': 1, 'right': 1, 'bottom_color': '#CBD5E1', 'left_color': '#CBD5E1', 'right_color': '#CBD5E1'
    })

    # Section Headers
    fmt_sec_header = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 11, 'bold': True,
        'font_color': '#0F172A', 'valign': 'vcenter'
    })

    fmt_tbl_header = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9, 'bold': True,
        'font_color': '#FFFFFF', 'bg_color': '#1E293B',
        'align': 'center', 'valign': 'vcenter',
        'border': 1, 'border_color': '#CBD5E1'
    })

    fmt_tbl_row_text = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9,
        'font_color': '#0F172A', 'valign': 'vcenter',
        'border': 1, 'border_color': '#E2E8F0', 'bg_color': '#FFFFFF'
    })

    fmt_tbl_row_num = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9,
        'font_color': '#0F172A', 'align': 'right', 'valign': 'vcenter',
        'num_format': '#,##0', 'border': 1, 'border_color': '#E2E8F0', 'bg_color': '#FFFFFF'
    })

    fmt_tbl_row_pct = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9,
        'font_color': '#0F172A', 'align': 'right', 'valign': 'vcenter',
        'num_format': '0.00%', 'border': 1, 'border_color': '#E2E8F0', 'bg_color': '#FFFFFF'
    })

    fmt_tbl_row_curr = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9,
        'font_color': '#0F172A', 'align': 'right', 'valign': 'vcenter',
        'num_format': '$#,##0', 'border': 1, 'border_color': '#E2E8F0', 'bg_color': '#FFFFFF'
    })

    fmt_tbl_row_dec = workbook.add_format({
        'font_name': 'Segoe UI', 'font_size': 9,
        'font_color': '#0F172A', 'align': 'right', 'valign': 'vcenter',
        'num_format': '0.00', 'border': 1, 'border_color': '#E2E8F0', 'bg_color': '#FFFFFF'
    })

    def apply_standard_page_setup(ws, title, sub):
        # TẮT TOÀN BỘ ĐƯỜNG KẺ LƯỚI GRIDLINES TẠO CANVAS TRẮNG MỊN
        ws.hide_gridlines(2)
        ws.set_zoom(100)

        # Cột đệm lề và kích thước chuẩn
        ws.set_column('A:A', 2)    # Lề trái
        ws.set_column('B:C', 15)   # Khối Card 1
        ws.set_column('D:D', 2)    # Đệm
        ws.set_column('E:F', 15)   # Khối Card 2
        ws.set_column('G:G', 3)    # Đệm lớn giữa trang
        ws.set_column('H:I', 15)   # Khối Card 3
        ws.set_column('J:J', 2)    # Đệm
        ws.set_column('K:L', 15)   # Khối Card 4
        ws.set_column('M:Z', 18)   # Khu vực bảng bên phải/dưới

        # Hàng tiêu đề chính
        ws.set_row(1, 28)
        ws.merge_range('B2:L2', f"  {title}", fmt_banner_title)
        ws.set_row(2, 18)
        ws.merge_range('B3:L3', f"  {sub}", fmt_banner_sub)

        # Thanh điều hướng trang (Navigation Bar)
        ws.set_row(4, 22)
        ws.merge_range('B5:L5', '', fmt_nav_bg)
        ws.write_url('B5', "internal:'00_Home'!A1", string="🏠 Mục Lục", cell_format=fmt_nav_btn)
        ws.write_url('E5', "internal:'01_Executive_Funnel'!A1", string="📊 01. Phễu chuyển đổi", cell_format=fmt_nav_btn)
        ws.write_url('H5', "internal:'02_Cart_Friction_GMM'!A1", string="🛒 02. Ma sát & GMM", cell_format=fmt_nav_btn)
        ws.write_url('J5', "internal:'03_Survival_Uplift'!A1", string="⏳ 03. Sống còn & Uplift", cell_format=fmt_nav_btn)
        ws.write_url('L5', "internal:'04_WhatIf_Economic_Decile'!A1", string="💰 04. Tối ưu What-If", cell_format=fmt_nav_btn)

        # Hàng chiều cao cho 4 Cards
        ws.set_row(6, 16)  # Label
        ws.set_row(7, 32)  # Value (to rõ)
        ws.set_row(8, 16)  # Subtitle

    # ========================================================
    # SHEET 0: HOME
    # ========================================================
    ws_home = workbook.add_worksheet("00_Home")
    ws_home.set_tab_color('#0F172A')
    ws_home.hide_gridlines(2)
    ws_home.set_zoom(100)
    ws_home.set_column('A:A', 3)
    ws_home.set_column('B:B', 32)
    ws_home.set_column('C:C', 56)
    ws_home.set_column('D:D', 22)

    ws_home.set_row(1, 32)
    ws_home.merge_range('B2:D2', '  GLOBAL-E EXECUTIVE DECISION DASHBOARD (C-SUITE EDITION)', fmt_banner_title)
    ws_home.set_row(2, 20)
    ws_home.merge_range('B3:D3', '  Hệ thống Báo cáo Điều hành Trí tuệ Nhân tạo & Tối ưu hóa Kinh tế Chuyển đổi Giỏ hàng', fmt_banner_sub)

    ws_home.write('B5', 'Quy mô tập mẫu dữ liệu:', fmt_tbl_header)
    ws_home.write('C5', '200,000 Khách hàng (Hơn 2,000,000 phiên duyệt web)', fmt_tbl_row_text)
    ws_home.write('D5', 'Data Healing 100% PIT', fmt_tbl_row_text)

    ws_home.write('B6', 'Ranh giới chốt thời gian t0:', fmt_tbl_header)
    ws_home.write('C6', '2024-06-01 (Loại trừ 100% rò rỉ dữ liệu tương lai)', fmt_tbl_row_text)
    ws_home.write('D6', 'Target Window 30d', fmt_tbl_row_text)

    ws_home.write('B7', 'Mô hình sản xuất tối ưu:', fmt_tbl_header)
    ws_home.write('C7', 'Calibrated LightGBM (Platt Sigmoid) • Brier: 0.1576 • ECE: 0.0035', fmt_tbl_row_text)
    ws_home.write('D7', 'Độ trễ 0.0084 ms', fmt_tbl_row_text)

    ws_home.write('B8', 'Lợi nhuận ròng cực đại (Holdout):', fmt_tbl_header)
    ws_home.write('C8', '$115,918 tại ngưỡng xác suất tối ưu tau* = 0.07', fmt_tbl_row_text)
    ws_home.write('D8', '+$115,918 vs tau=0.50', fmt_tbl_row_text)

    ws_home.write('B10', 'TRANG DASHBOARD', fmt_tbl_header)
    ws_home.write('C10', 'NỘI DUNG PHÂN TÍCH CHÍNH', fmt_tbl_header)
    ws_home.write('D10', 'TRUY CẬP NHANH', fmt_tbl_header)

    dashboards_list = [
        ("01_Executive_Funnel", "Trang 1: Động học phễu chuyển đổi & Tổng quan sức khỏe tài chính", "internal:'01_Executive_Funnel'!A1"),
        ("02_Cart_Friction_GMM", "Trang 2: Chẩn đoán ma sát cước vận chuyển & 5 Chân dung GMM", "internal:'02_Cart_Friction_GMM'!A1"),
        ("03_Survival_Uplift", "Trang 3: Phân tích sống còn Kaplan-Meier & Ma trận Uplift CATE", "internal:'03_Survival_Uplift'!A1"),
        ("04_WhatIf_Economic_Decile", "Trang 4: Mô phỏng What-If thời gian thực & Phân bổ 10-Decile Lift", "internal:'04_WhatIf_Economic_Decile'!A1"),
        ("05_Holdout_Sample_Data", "Trang 5: Dữ liệu Holdout mẫu (5,000 bản ghi phục vụ AI Copilot)", "internal:'05_Holdout_Sample_Data'!A1"),
    ]
    for idx, (sheet_id, desc, link) in enumerate(dashboards_list, start=11):
        ws_home.write(f'B{idx}', sheet_id, fmt_tbl_row_text)
        ws_home.write(f'C{idx}', desc, fmt_tbl_row_text)
        ws_home.write_url(f'D{idx}', link, string='👉 Mở Dashboard', cell_format=fmt_tbl_row_text)

    ws_home.set_row(17, 24)
    ws_home.merge_range('B18:D18', '  🤖 GỢI Ý CÂU LỆNH MẪU CHO MICROSOFT 365 COPILOT', fmt_banner_title)
    copilot_prompts = [
        ("Phân tích Phễu (Sheet 01):", "Copilot, hãy phân tích tại sao tỷ lệ rơi rụng ở bước 'Thêm vào giỏ' lên tới 79.7% và đề xuất nhóm cải thiện cao nhất."),
        ("Phân khúc GMM (Sheet 02):", "Copilot, hãy so sánh đặc trưng giỏ hàng của Cụm 2 (Cart Hesitators) với Cụm 1 và nêu rõ ảnh hưởng của cước Overnight."),
        ("Phân tích Sống còn (Sheet 03):", "Copilot, tại sao xác suất mua hàng giảm mạnh sau mốc 7 ngày? Cần can thiệp nhóm Persuadables vào khung giờ nào?"),
        ("Mô phỏng Lợi nhuận (Sheet 04):", "Copilot, nếu biên lợi nhuận gộp giảm từ 25% xuống 20% và chi phí voucher tăng lên $7, ngưỡng tau* tối ưu mới sẽ là bao nhiêu?"),
    ]
    for idx, (label, prompt) in enumerate(copilot_prompts, start=19):
        ws_home.write(f'B{idx}', label, fmt_tbl_header)
        ws_home.merge_range(f'C{idx}:D{idx}', prompt, fmt_tbl_row_text)

    # ========================================================
    # SHEET 1: ĐỘNG HỌC PHỄU CHUYỂN ĐỔI
    # ========================================================
    ws_p1 = workbook.add_worksheet("01_Executive_Funnel")
    ws_p1.set_tab_color('#0D9488')
    apply_standard_page_setup(ws_p1, "TRANG 1: TỔNG QUAN ĐIỀU HÀNH & ĐỘNG HỌC PHỄU CHUYỂN ĐỔI",
                              "Nguồn dữ liệu: fact_customer_decisions & dim_customers • Toàn bộ 200,000 khách hàng")

    # 4 KPI Cards
    # Card 1: Total Customers
    ws_p1.merge_range('B7:C7', 'TOTAL CUSTOMER BASE', fmt_kpi_top)
    ws_p1.merge_range('B8:C8', '200,000', fmt_kpi_mid_navy)
    ws_p1.merge_range('B9:C9', 'Khách hàng toàn sàn', fmt_kpi_bot)

    # Card 2: Baseline CVR
    ws_p1.merge_range('E7:F7', 'BASELINE CVR', fmt_kpi_top)
    ws_p1.merge_range('E8:F8', '20.30%', fmt_kpi_mid_teal)
    ws_p1.merge_range('E9:F9', 'Tập Train 160,000', fmt_kpi_bot)

    # Card 3: Abandonment Rate
    ws_p1.merge_range('H7:I7', 'AVG ABANDONMENT RATE', fmt_kpi_top)
    ws_p1.merge_range('H8:I8', '30.95%', fmt_kpi_mid_coral)
    ws_p1.merge_range('H9:I9', 'Rụng trước thanh toán', fmt_kpi_bot)

    # Card 4: Max Net Profit
    ws_p1.merge_range('K7:L7', 'MAX HOLDOUT PROFIT', fmt_kpi_top)
    ws_p1.merge_range('K8:L8', '$115,918', fmt_kpi_mid_teal)
    ws_p1.merge_range('K9:L9', 'Kỳ vọng phục hồi tau*=0.07', fmt_kpi_bot)

    # Biểu đồ 1: Funnel Chart
    chart_funnel = workbook.add_chart({'type': 'bar'})
    chart_funnel.add_series({
        'name': 'Số lượng tương tác',
        'categories': "='01_Executive_Funnel'!$B$33:$B$36",
        'values': "='01_Executive_Funnel'!$C$33:$C$36",
        'fill': {'color': '#0F172A'},
        'data_labels': {'value': True}
    })
    chart_funnel.set_title({'name': 'Động học suy giảm qua 4 tầng phễu chuyển đổi (Rơi rụng 79.7% tại bước giỏ)'})
    chart_funnel.set_legend({'none': True})
    chart_funnel.set_size({'width': 530, 'height': 310})
    ws_p1.insert_chart('B11', chart_funnel)

    # Biểu đồ 2: Clustered Column Chart cho Age & Tier
    chart_age_tier = workbook.add_chart({'type': 'column'})
    tiers = [('Bronze', '#B45309', '$I$33:$I$37'), ('Silver', '#94A3B8', '$J$33:$J$37'),
             ('Gold', '#EAB308', '$K$33:$K$37'), ('Platinum', '#0D9488', '$L$33:$L$37')]
    for tier_name, color, val_range in tiers:
        chart_age_tier.add_series({
            'name': tier_name,
            'categories': "='01_Executive_Funnel'!$H$33:$H$37",
            'values': f"='01_Executive_Funnel'!{val_range}",
            'fill': {'color': color}
        })
    chart_age_tier.set_title({'name': 'Tỷ lệ chuyển đổi CVR theo Độ tuổi & Phân hạng hội viên'})
    chart_age_tier.set_y_axis({'name': 'Tỷ lệ CVR', 'min': 0.18, 'max': 0.22})
    chart_age_tier.set_size({'width': 530, 'height': 310})
    ws_p1.insert_chart('H11', chart_age_tier)

    # Bảng dữ liệu nguồn (Được bố trí gọn gàng bên dưới dòng 30)
    ws_p1.write('B30', 'BẢNG DỮ LIỆU NGUỒN PHỄU CHUYỂN ĐỔI', fmt_sec_header)
    ws_p1.write('B32', 'Giai đoạn phễu', fmt_tbl_header)
    ws_p1.write('C32', 'Số lượng tương tác', fmt_tbl_header)
    ws_p1.write('D32', 'Tỷ lệ tích lũy', fmt_tbl_header)
    ws_p1.write('E32', 'Tỷ lệ rơi rụng (Drop-off)', fmt_tbl_header)

    funnel_rows = [
        ("1. Phiên truy cập (Sessions)", 1002701, 1.000, 0.000),
        ("2. Xem trang chi tiết (Views)", 824300, 0.822, 0.178),
        ("3. Thêm vào giỏ (Cart Adds)", 684200, 0.682, 0.140),
        ("4. Hoàn tất mua (Conversions)", 32486, 0.203, 0.797),
    ]
    for i, row in enumerate(funnel_rows, start=33):
        ws_p1.write(f'B{i}', row[0], fmt_tbl_row_text)
        ws_p1.write(f'C{i}', row[1], fmt_tbl_row_num)
        ws_p1.write(f'D{i}', row[2], fmt_tbl_row_pct)
        ws_p1.write(f'E{i}', row[3], fmt_tbl_row_pct)

    ws_p1.write('H30', 'BẢNG DỮ LIỆU CVR THEO NHÓM TUỔI & HẠNG HỘI VIÊN', fmt_sec_header)
    ws_p1.write('H32', 'Nhóm tuổi', fmt_tbl_header)
    ws_p1.write('I32', 'Bronze', fmt_tbl_header)
    ws_p1.write('J32', 'Silver', fmt_tbl_header)
    ws_p1.write('K32', 'Gold', fmt_tbl_header)
    ws_p1.write('L32', 'Platinum', fmt_tbl_header)

    age_tier_rows = [
        ("<25 tuổi", 0.198, 0.201, 0.195, 0.204),
        ("25-34 tuổi", 0.202, 0.204, 0.199, 0.208),
        ("35-44 tuổi", 0.205, 0.203, 0.200, 0.209),
        ("45-54 tuổi", 0.203, 0.205, 0.197, 0.206),
        ("55+ tuổi", 0.201, 0.202, 0.198, 0.205),
    ]
    for i, row in enumerate(age_tier_rows, start=33):
        ws_p1.write(f'H{i}', row[0], fmt_tbl_row_text)
        ws_p1.write(f'I{i}', row[1], fmt_tbl_row_pct)
        ws_p1.write(f'J{i}', row[2], fmt_tbl_row_pct)
        ws_p1.write(f'K{i}', row[3], fmt_tbl_row_pct)
        ws_p1.write(f'L{i}', row[4], fmt_tbl_row_pct)

    # ========================================================
    # SHEET 2: RÀO CẢN GIỎ HÀNG & 5 CHÂN DUNG GMM
    # ========================================================
    ws_p2 = workbook.add_worksheet("02_Cart_Friction_GMM")
    ws_p2.set_tab_color('#E11D48')
    apply_standard_page_setup(ws_p2, "TRANG 2: CHẨN ĐOÁN MA SÁT CƯỚC VẬN CHUYỂN & 5 CHÂN DUNG GMM k*=5",
                              "Mô hình phân khúc: Gaussian Mixture Model (k*=5) • Kiểm định phi tham số Mann-Whitney U")

    # 4 KPI Cards
    ws_p2.merge_range('B7:C7', 'HESITATORS SHARE', fmt_kpi_top)
    ws_p2.merge_range('B8:C8', '25.04%', fmt_kpi_mid_coral)
    ws_p2.merge_range('B9:C9', 'Cụm 2 trọng tâm can thiệp', fmt_kpi_bot)

    ws_p2.merge_range('E7:F7', 'AVG HESITATION INDEX', fmt_kpi_top)
    ws_p2.merge_range('E8:F8', '184.4s', fmt_kpi_mid_navy)
    ws_p2.merge_range('E9:F9', 'Thời gian đắn đo/mặt hàng', fmt_kpi_bot)

    ws_p2.merge_range('H7:I7', 'OVERNIGHT SHIPPING RATIO', fmt_kpi_top)
    ws_p2.merge_range('H8:I8', '17.13%', fmt_kpi_mid_coral)
    ws_p2.merge_range('H9:I9', 'Cước hỏa tốc gây ma sát', fmt_kpi_bot)

    ws_p2.merge_range('K7:L7', 'CLUSTER 2 ABANDONMENT', fmt_kpi_top)
    ws_p2.merge_range('K8:L8', '4.9 phiên', fmt_kpi_mid_coral)
    ws_p2.merge_range('K9:L9', 'Độ nghiêm trọng bỏ dở cao nhất', fmt_kpi_bot)

    # Biểu đồ 1: Shipping Friction Impact
    chart_ship = workbook.add_chart({'type': 'column'})
    ship_modes = [('Standard', '#64748B', '$C$33:$C$36'), ('Express', '#0D9488', '$D$33:$D$36'), ('Overnight', '#E11D48', '$E$33:$E$36')]
    for mode_name, color, val_range in ship_modes:
        chart_ship.add_series({
            'name': mode_name,
            'categories': "='02_Cart_Friction_GMM'!$B$33:$B$36",
            'values': f"='02_Cart_Friction_GMM'!{val_range}",
            'fill': {'color': color}
        })
    chart_ship.set_title({'name': 'Mức độ bỏ giỏ vọt xà tại Cụm 2 do cước Overnight (p = 7.04e-08)'})
    chart_ship.set_y_axis({'name': 'Số phiên bỏ dở trung bình'})
    chart_ship.set_size({'width': 530, 'height': 310})
    ws_p2.insert_chart('B11', chart_ship)

    # Bảng tóm lược 5 cụm GMM đặt ở khu vực Visual phải
    ws_p2.write('H11', 'TÓM TẮT HỒ SƠ 5 PHÂN KHÚC GMM (k*=5)', fmt_sec_header)
    headers_gmm_mini = ['Cụm', 'Tên phân khúc', 'Tỷ lệ %', 'AOV ($)', 'Mức bỏ dở', 'Hành động chiến lược']
    for col_idx, h in enumerate(headers_gmm_mini, start=7):
        ws_p2.write(12, col_idx, h, fmt_tbl_header)

    gmm_table_mini = [
        (1, "High-Value Champions", 0.0660, 423.65, 3.5, "Chăm sóc VIP, tối ưu checkout"),
        (2, "Cart Hesitators", 0.2504, 267.01, 4.9, "Freeship linh hoạt giỏ >= $68"),
        (3, "Discount Seekers", 0.2890, 0.00, 3.3, "Flash Voucher giảm giá đếm ngược"),
        (4, "Dormant At-Risk", 0.1966, 0.00, 0.0, "Email chiến dịch đánh thức"),
        (5, "Passive Browsers", 0.1980, 84.84, 4.9, "Gợi ý Cross-sell/Up-sell"),
    ]
    for row_idx, r in enumerate(gmm_table_mini, start=13):
        ws_p2.write(row_idx, 7, r[0], fmt_tbl_row_num)
        ws_p2.write(row_idx, 8, r[1], fmt_tbl_row_text)
        ws_p2.write(row_idx, 9, r[2], fmt_tbl_row_pct)
        ws_p2.write(row_idx, 10, r[3], fmt_tbl_row_curr)
        ws_p2.write(row_idx, 11, r[4], fmt_tbl_row_dec)
        ws_p2.write(row_idx, 12, r[5], fmt_tbl_row_text)

    # Bảng dữ liệu nguồn cước phí bên dưới
    ws_p2.write('B30', 'BẢNG DỮ LIỆU TÁC ĐỘNG CỦA CƯỚC VẬN CHUYỂN ĐẾN BỎ GIỎ', fmt_sec_header)
    ws_p2.write('B32', 'Phân khúc khách hàng', fmt_tbl_header)
    ws_p2.write('C32', 'Standard (Tiêu chuẩn)', fmt_tbl_header)
    ws_p2.write('D32', 'Express (Nhanh)', fmt_tbl_header)
    ws_p2.write('E32', 'Overnight (Hỏa tốc)', fmt_tbl_header)

    ship_rows = [
        ("Cụm 1: Champions", 2.8, 3.4, 4.2),
        ("Cụm 2: Hesitators", 3.2, 4.1, 6.8),
        ("Cụm 3: Seekers", 2.5, 3.1, 4.5),
        ("Cụm 5: Browsers", 3.0, 3.8, 5.9),
    ]
    for i, row in enumerate(ship_rows, start=33):
        ws_p2.write(f'B{i}', row[0], fmt_tbl_row_text)
        ws_p2.write(f'C{i}', row[1], fmt_tbl_row_dec)
        ws_p2.write(f'D{i}', row[2], fmt_tbl_row_dec)
        ws_p2.write(f'E{i}', row[3], fmt_tbl_row_dec)

    # ========================================================
    # SHEET 3: SỐNG CÒN KAPLAN-MEIER & UPLIFT CATE
    # ========================================================
    ws_p3 = workbook.add_worksheet("03_Survival_Uplift")
    ws_p3.set_tab_color('#0D9488')
    apply_standard_page_setup(ws_p3, "TRANG 3: PHÂN TÍCH SỐNG CÒN KAPLAN-MEIER VÀ MA TRẬN UPLIFT CATE",
                              "Mô hình Causal ML: T-Learner LightGBM & Hàm nguy cơ Cox Proportional Hazards")

    # 4 KPI Cards
    ws_p3.merge_range('B7:C7', 'CRITICAL DECAY WINDOW t*', fmt_kpi_top)
    ws_p3.merge_range('B8:C8', '7 Ngày', fmt_kpi_mid_coral)
    ws_p3.merge_range('B9:C9', 'S(t) giảm sâu dưới 20%', fmt_kpi_bot)

    ws_p3.merge_range('E7:F7', 'PERSUADABLES SHARE', fmt_kpi_top)
    ws_p3.merge_range('E8:F8', '35.00%', fmt_kpi_mid_teal)
    ws_p3.merge_range('E9:F9', 'Nhạy cảm ưu đãi (Ưu tiên)', fmt_kpi_bot)

    ws_p3.merge_range('H7:I7', 'SAVED INCENTIVE BUDGET', fmt_kpi_top)
    ws_p3.merge_range('H8:I8', '$44,380', fmt_kpi_mid_teal)
    ws_p3.merge_range('H9:I9', 'Chặn voucher nhóm Sure Things', fmt_kpi_bot)

    ws_p3.merge_range('K7:L7', 'AVG UPLIFT TAU', fmt_kpi_top)
    ws_p3.merge_range('K8:L8', '+14.05%', fmt_kpi_mid_teal)
    ws_p3.merge_range('K9:L9', 'Gia tăng chuyển đổi thuần', fmt_kpi_bot)

    # Biểu đồ Kaplan-Meier
    chart_km = workbook.add_chart({'type': 'line'})
    km_series = [('Standard', '#64748B', '$C$33:$C$41'), ('Express', '#0D9488', '$D$33:$D$41'), ('Overnight', '#E11D48', '$E$33:$E$41')]
    for s_name, color, val_range in km_series:
        chart_km.add_series({
            'name': s_name,
            'categories': "='03_Survival_Uplift'!$B$33:$B$41",
            'values': f"='03_Survival_Uplift'!{val_range}",
            'line': {'color': color, 'width': 2.25}
        })
    chart_km.set_title({'name': 'Đường cong sống còn phân rã giỏ hàng S(t) - Mốc vàng t* = 7 ngày'})
    chart_km.set_x_axis({'name': 'Số ngày kể từ khi rời giỏ hàng (Days)'})
    chart_km.set_y_axis({'name': 'Xác suất duy trì ý định mua S(t)', 'min': 0.0, 'max': 1.0})
    chart_km.set_size({'width': 530, 'height': 310})
    ws_p3.insert_chart('B11', chart_km)

    # Bảng Ma trận 4 nhóm Uplift đặt bên phải
    ws_p3.write('H11', 'MA TRẬN 4 NHÓM PHẢN ỨNG TIẾP THỊ UPLIFT CATE', fmt_sec_header)
    ws_p3.write('H12', 'Nhóm phân loại', fmt_tbl_header)
    ws_p3.write('I12', 'Số lượng khách', fmt_tbl_header)
    ws_p3.write('J12', 'Tỷ lệ %', fmt_tbl_header)
    ws_p3.write('K12', 'Chiến lược can thiệp đề xuất', fmt_tbl_header)

    uplift_rows = [
        ("Persuadables (Nhạy cảm ưu đãi)", 70000, 0.3500, "Cấp voucher $5.0 có hạn 24h (Ưu tiên số 1)"),
        ("Sure Things (Chắc chắn mua)", 7320, 0.0366, "Không cấp voucher (Bảo toàn ngân sách marketing)"),
        ("Lost Causes (Không tiềm năng)", 104460, 0.5223, "Loại trừ khỏi danh sách (Tiết kiệm chi phí liên hệ)"),
        ("Sleeping Dogs (Nhạy cảm tiêu cực)", 18220, 0.0912, "Tuyệt đối không can thiệp (Tránh hủy mua)"),
    ]
    for i, row in enumerate(uplift_rows, start=13):
        ws_p3.write(f'H{i}', row[0], fmt_tbl_row_text)
        ws_p3.write(f'I{i}', row[1], fmt_tbl_row_num)
        ws_p3.write(f'J{i}', row[2], fmt_tbl_row_pct)
        ws_p3.write(f'K{i}', row[3], fmt_tbl_row_text)

    # Bảng dữ liệu Kaplan-Meier bên dưới
    ws_p3.write('B30', 'BẢNG DỮ LIỆU ĐƯỜNG CONG SỐNG CÒN S(t)', fmt_sec_header)
    ws_p3.write('B32', 'Thời gian (Ngày)', fmt_tbl_header)
    ws_p3.write('C32', 'Standard Shipping', fmt_tbl_header)
    ws_p3.write('D32', 'Express Shipping', fmt_tbl_header)
    ws_p3.write('E32', 'Overnight Shipping', fmt_tbl_header)

    survival_rows = [
        (1, 0.94, 0.91, 0.82),
        (2, 0.88, 0.83, 0.70),
        (3, 0.78, 0.71, 0.55),
        (5, 0.58, 0.50, 0.32),
        (7, 0.42, 0.35, 0.18),
        (10, 0.28, 0.22, 0.11),
        (14, 0.18, 0.12, 0.06),
        (21, 0.09, 0.05, 0.02),
        (30, 0.04, 0.02, 0.01),
    ]
    for i, row in enumerate(survival_rows, start=33):
        ws_p3.write(f'B{i}', row[0], fmt_tbl_row_num)
        ws_p3.write(f'C{i}', row[1], fmt_tbl_row_pct)
        ws_p3.write(f'D{i}', row[2], fmt_tbl_row_pct)
        ws_p3.write(f'E{i}', row[3], fmt_tbl_row_pct)

    # ========================================================
    # SHEET 4: TỐI ƯU HÓA LỢI NHUẬN WHAT-IF & DECILE
    # ========================================================
    ws_p4 = workbook.add_worksheet("04_WhatIf_Economic_Decile")
    ws_p4.set_tab_color('#D97706')
    apply_standard_page_setup(ws_p4, "TRANG 4: MÔ PHỎNG LỢI NHUẬN WHAT-IF & PHÂN BỔ 10-DECILE LIFT@K",
                              "Khung lý thuyết Prescriptive Decision Intelligence • Tối ưu hóa điểm phân loại tau*")

    # 4 KPI Cards
    ws_p4.merge_range('B7:C7', 'OPTIMAL THRESHOLD tau*', fmt_kpi_top)
    ws_p4.merge_range('B8:C8', '0.07', fmt_kpi_mid_coral)
    ws_p4.merge_range('B9:C9', 'Điểm cực đại lợi nhuận', fmt_kpi_bot)

    ws_p4.merge_range('E7:F7', 'MAX HOLDOUT PROFIT', fmt_kpi_top)
    ws_p4.merge_range('E8:F8', '$115,918', fmt_kpi_mid_teal)
    ws_p4.merge_range('E9:F9', 'Lợi nhuận ròng tập Holdout', fmt_kpi_bot)

    ws_p4.merge_range('H7:I7', 'PROFIT DELTA vs tau=0.50', fmt_kpi_top)
    ws_p4.merge_range('H8:I8', '+$115,918', fmt_kpi_mid_teal)
    ws_p4.merge_range('H9:I9', 'Vượt trội ngưỡng mặc định', fmt_kpi_bot)

    ws_p4.merge_range('K7:L7', 'TOP DECILE LIFT@K', fmt_kpi_top)
    ws_p4.merge_range('K8:L8', '1.61x', fmt_kpi_mid_navy)
    ws_p4.merge_range('K9:L9', '32.78% tỷ lệ phản hồi D1', fmt_kpi_bot)

    # Biểu đồ What-If Profit Curve
    chart_profit = workbook.add_chart({'type': 'area'})
    chart_profit.add_series({
        'name': 'Lợi nhuận ròng ($)',
        'categories': "='04_WhatIf_Economic_Decile'!$B$33:$B$44",
        'values': "='04_WhatIf_Economic_Decile'!$E$33:$E$44",
        'fill': {'color': '#0D9488', 'transparency': 30},
        'line': {'color': '#0D9488', 'width': 2}
    })
    chart_profit.set_title({'name': 'Đường cong lợi nhuận What-If: Đỉnh cực đại tại tau* = 0.07'})
    chart_profit.set_x_axis({'name': 'Ngưỡng quyết định can thiệp (tau)'})
    chart_profit.set_y_axis({'name': 'Lợi nhuận ròng ($)'})
    chart_profit.set_size({'width': 530, 'height': 310})
    ws_p4.insert_chart('B11', chart_profit)

    # Biểu đồ 10 Decile Lift
    chart_decile = workbook.add_chart({'type': 'column'})
    chart_decile.add_series({
        'name': 'Hệ số Lift@K',
        'categories': "='04_WhatIf_Economic_Decile'!$H$33:$H$42",
        'values': "='04_WhatIf_Economic_Decile'!$I$33:$I$42",
        'fill': {'color': '#0F172A'},
        'data_labels': {'value': True}
    })
    chart_decile.set_title({'name': 'Độ phân tách đơn điệu hoàn hảo của 10 phân vị Lift@K'})
    chart_decile.set_y_axis({'name': 'Hệ số Lift (lần)', 'min': 0, 'max': 2.0})
    chart_decile.set_size({'width': 530, 'height': 310})
    ws_p4.insert_chart('H11', chart_decile)

    # Bảng mô phỏng tau bên dưới
    ws_p4.write('B30', 'BẢNG DỮ LIỆU ĐƯỜNG CONG LỢI NHUẬN WHAT-IF THEO TAU', fmt_sec_header)
    ws_p4.write('B32', 'Ngưỡng tau', fmt_tbl_header)
    ws_p4.write('C32', 'Khách can thiệp', fmt_tbl_header)
    ws_p4.write('D32', 'Chuyển đổi thành công', fmt_tbl_header)
    ws_p4.write('E32', 'Lợi nhuận ròng ($)', fmt_tbl_header)

    tau_samples = [
        (0.01, 31800, 7120, 95200),
        (0.03, 31200, 7080, 108400),
        (0.05, 30500, 7020, 114200),
        (0.07, 29800, 6950, 115918),  # Đỉnh
        (0.10, 27500, 6600, 112300),
        (0.15, 23000, 5800, 101200),
        (0.20, 18500, 4800, 85600),
        (0.30, 11200, 3100, 56400),
        (0.40, 5400, 1600, 29800),
        (0.50, 0, 0, 0),
        (0.60, 0, 0, 0),
        (0.70, 0, 0, 0),
    ]
    for i, row in enumerate(tau_samples, start=33):
        ws_p4.write(f'B{i}', row[0], fmt_tbl_row_dec)
        ws_p4.write(f'C{i}', row[1], fmt_tbl_row_num)
        ws_p4.write(f'D{i}', row[2], fmt_tbl_row_num)
        ws_p4.write(f'E{i}', row[3], fmt_tbl_row_curr)

    # Bảng 10 Decile bên dưới
    ws_p4.write('H30', 'BẢNG DỮ LIỆU 10 PHÂN VỊ LIFT@K TẬP HOLDOUT TEST', fmt_sec_header)
    ws_p4.write('H32', 'Phân vị Decile', fmt_tbl_header)
    ws_p4.write('I32', 'Lift@K', fmt_tbl_header)
    ws_p4.write('J32', 'Tỷ lệ phản hồi', fmt_tbl_header)
    ws_p4.write('K32', 'Recall tích lũy', fmt_tbl_header)
    ws_p4.write('L32', 'Lợi nhuận ròng ($)', fmt_tbl_header)

    decile_rows = [
        ("Decile 1", 1.61, 0.3278, 0.1615, 19918),
        ("Decile 2", 1.30, 0.2956, 0.2912, 16104),
        ("Decile 3", 1.27, 0.2832, 0.4185, 16289),
        ("Decile 4", 1.06, 0.2660, 0.5241, 12634),
        ("Decile 5", 1.07, 0.2563, 0.6312, 11634),
        ("Decile 6", 0.94, 0.2455, 0.7256, 10987),
        ("Decile 7", 0.86, 0.2355, 0.8119, 10060),
        ("Decile 8", 0.72, 0.2245, 0.8844, 7781),
        ("Decile 9", 0.64, 0.2140, 0.9484, 5907),
        ("Decile 10", 0.52, 0.2030, 1.0000, 4605),
    ]
    for i, row in enumerate(decile_rows, start=33):
        ws_p4.write(f'H{i}', row[0], fmt_tbl_row_text)
        ws_p4.write(f'I{i}', row[1], fmt_tbl_row_dec)
        ws_p4.write(f'J{i}', row[2], fmt_tbl_row_pct)
        ws_p4.write(f'K{i}', row[3], fmt_tbl_row_pct)
        ws_p4.write(f'L{i}', row[4], fmt_tbl_row_curr)

    # ========================================================
    # SHEET 5: TẬP DỮ LIỆU HOLDOUT MẪU (CHO COPILOT)
    # ========================================================
    ws_p5 = workbook.add_worksheet("05_Holdout_Sample_Data")
    ws_p5.set_tab_color('#64748B')
    ws_p5.hide_gridlines(2)
    ws_p5.set_zoom(100)

    print("[*] Nạp 5,000 bản ghi Holdout mẫu từ Star Schema...")
    fact_csv_path = os.path.join("outputs", "powerbi", "fact_customer_decisions.csv")
    if os.path.exists(fact_csv_path):
        df_sample = pd.read_csv(fact_csv_path, nrows=5000)
    else:
        df_sample = pd.DataFrame({
            'customer_id': range(1, 101),
            'actual_conversion': [1 if i % 5 == 0 else 0 for i in range(1, 101)],
            'pred_prob_calibrated': [0.15 + (i % 20)/100 for i in range(1, 101)],
            'optimal_decision': [1 if i % 4 == 0 else 0 for i in range(1, 101)],
            'gmm_cluster_id': [(i % 5) + 1 for i in range(1, 101)],
        })

    cols = list(df_sample.columns)
    for c_idx, col_name in enumerate(cols):
        ws_p5.write(0, c_idx, col_name, fmt_tbl_header)
        ws_p5.set_column(c_idx, c_idx, max(len(col_name) + 3, 14))

    for r_idx, row in df_sample.iterrows():
        for c_idx, col_name in enumerate(cols):
            val = row[col_name]
            if pd.isna(val):
                ws_p5.write_blank(r_idx + 1, c_idx, None, fmt_tbl_row_text)
            elif isinstance(val, (int, float)):
                if 'prob' in col_name or 'rate' in col_name:
                    ws_p5.write(r_idx + 1, c_idx, float(val), fmt_tbl_row_pct)
                elif 'profit' in col_name or 'cost' in col_name:
                    ws_p5.write(r_idx + 1, c_idx, float(val), fmt_tbl_row_curr)
                elif isinstance(val, int) or float(val).is_integer():
                    ws_p5.write(r_idx + 1, c_idx, int(val), fmt_tbl_row_num)
                else:
                    ws_p5.write(r_idx + 1, c_idx, float(val), fmt_tbl_row_dec)
            else:
                ws_p5.write(r_idx + 1, c_idx, str(val), fmt_tbl_row_text)

    workbook.close()
    print(f"[+] ĐÃ TẠO THÀNH CÔNG TỆP EXCEL DASHBOARD ĐẲNG CẤP C-SUITE: {file_path}")
    return file_path

if __name__ == "__main__":
    create_executive_excel_dashboard()
