"""
Script: generate_pbir_dashboards.py
Mục đích: Tự động khởi tạo toàn bộ 4 trang Dashboard và các Visuals trong
          định dạng chuẩn Microsoft Power BI Enhanced Report Format (PBIR v2)
          thuộc dự án dashboards.pbip với phong cách thiết kế Executive SaaS
          chuyên nghiệp, sang trọng, đầy đủ dữ liệu chiều sâu giống như web.
"""

import os
import sys
import json
import shutil

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

REPORT_DEF_DIR = os.path.join("outputs", "powerbi", "dashboards.Report", "definition")
PAGES_DIR = os.path.join(REPORT_DEF_DIR, "pages")

SCHEMA_CONTAINER = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json"
SCHEMA_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_PAGES_META = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json"

def _lit(val):
    return {"expr": {"Literal": {"Value": val}}}

def _solid(color_hex):
    return {"solid": {"color": _lit(f"'{color_hex}'")}}

def get_container_styling(title_text=None, subtitle_text=None):
    container_objs = {
        "background": [
            {
                "properties": {
                    "show": _lit("true"),
                    "color": _solid("#FFFFFF"),
                    "transparency": _lit("0D")
                }
            }
        ],
        "border": [
            {
                "properties": {
                    "show": _lit("true"),
                    "color": _solid("#E2E8F0"),
                    "radius": _lit("12D")
                }
            }
        ],
        "dropShadow": [
            {
                "properties": {
                    "show": _lit("true"),
                    "color": _solid("#0F172A"),
                    "transparency": _lit("92D"),
                    "shadowBlur": _lit("8D"),
                    "position": _lit("'Outer'")
                }
            }
        ]
    }
    if title_text:
        container_objs["title"] = [
            {
                "properties": {
                    "show": _lit("true"),
                    "text": _lit(f"'{title_text}'"),
                    "fontColor": _solid("#0F172A"),
                    "fontSize": _lit("12.5D"),
                    "bold": _lit("true"),
                    "fontFamily": _lit("'Segoe UI Semibold'")
                }
            }
        ]
    if subtitle_text:
        container_objs["subTitle"] = [
            {
                "properties": {
                    "show": _lit("true"),
                    "text": _lit(f"'{subtitle_text}'"),
                    "fontColor": _solid("#64748B"),
                    "fontSize": _lit("9.5D"),
                    "fontFamily": _lit("'Segoe UI'")
                }
            }
        ]
    return container_objs

def create_banner_visual(vis_id, x, y, width, height, banner_measure, subtitle_text):
    return {
        "$schema": SCHEMA_CONTAINER,
        "name": vis_id,
        "position": {
            "x": x, "y": y, "z": 50,
            "height": height, "width": width,
            "tabOrder": 50
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Entity": "fact_customer_decisions"}},
                                        "Property": banner_measure
                                    }
                                },
                                "queryRef": f"fact_customer_decisions.{banner_measure}"
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": {
                "background": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid("#0F172A"),
                            "transparency": _lit("0D")
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid("#1E293B"),
                            "radius": _lit("10D")
                        }
                    }
                ],
                "dropShadow": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid("#0F172A"),
                            "transparency": _lit("80D"),
                            "shadowBlur": _lit("8D")
                        }
                    }
                ]
            },
            "objects": {
                "labels": [
                    {
                        "properties": {
                            "color": _solid("#FFFFFF"),
                            "fontSize": _lit("14.5D"),
                            "fontFamily": _lit("'Segoe UI Bold'")
                        }
                    }
                ],
                "categoryLabels": [
                    {
                        "properties": {
                            "show": _lit("false")
                        }
                    }
                ]
            }
        }
    }

def create_card_visual(vis_id, x, y, width, height, entity, measure_name, title_text, sub_text, accent_color="#0D9488"):
    return {
        "$schema": SCHEMA_CONTAINER,
        "name": vis_id,
        "position": {
            "x": x, "y": y, "z": 100,
            "height": height, "width": width,
            "tabOrder": 100
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Entity": entity}},
                                        "Property": measure_name
                                    }
                                },
                                "queryRef": f"{entity}.{measure_name}"
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": {
                "background": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid("#FFFFFF"),
                            "transparency": _lit("0D")
                        }
                    }
                ],
                "border": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid(accent_color),
                            "radius": _lit("12D")
                        }
                    }
                ],
                "dropShadow": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid("#0F172A"),
                            "transparency": _lit("92D"),
                            "shadowBlur": _lit("8D"),
                            "position": _lit("'Outer'")
                        }
                    }
                ],
                "title": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "text": _lit(f"'{title_text}'"),
                            "fontColor": _solid("#64748B"),
                            "fontSize": _lit("9.5D"),
                            "bold": _lit("true"),
                            "fontFamily": _lit("'Segoe UI Bold'")
                        }
                    }
                ],
                "subTitle": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "text": _lit(f"'{sub_text}'"),
                            "fontColor": _solid("#475569"),
                            "fontSize": _lit("8.5D"),
                            "fontFamily": _lit("'Segoe UI'")
                        }
                    }
                ]
            },
            "objects": {
                "labels": [
                    {
                        "properties": {
                            "color": _solid(accent_color),
                            "fontSize": _lit("24D"),
                            "fontFamily": _lit("'Segoe UI Bold'")
                        }
                    }
                ],
                "categoryLabels": [
                    {
                        "properties": {
                            "show": _lit("false")
                        }
                    }
                ]
            }
        }
    }

def get_chart_objects(primary_color="#0D9488"):
    return {
        "dataPoint": [
            {
                "properties": {
                    "fill": _solid(primary_color)
                }
            }
        ],
        "categoryAxis": [
            {
                "properties": {
                    "show": _lit("true"),
                    "labelColor": _solid("#1E293B"),
                    "fontSize": _lit("10.5D"),
                    "fontFamily": _lit("'Segoe UI Semibold'")
                }
            }
        ],
        "valueAxis": [
            {
                "properties": {
                    "show": _lit("true"),
                    "labelColor": _solid("#64748B"),
                    "fontSize": _lit("9.5D"),
                    "fontFamily": _lit("'Segoe UI'"),
                    "gridlineShow": _lit("true"),
                    "gridlineColor": _solid("#F1F5F9")
                }
            }
        ],
        "labels": [
            {
                "properties": {
                    "show": _lit("true"),
                    "color": _solid("#0F172A"),
                    "fontSize": _lit("9.5D"),
                    "fontFamily": _lit("'Segoe UI Semibold'"),
                    "labelPosition": _lit("'OutsideEnd'")
                }
            }
        ],
        "legend": [
            {
                "properties": {
                    "show": _lit("true"),
                    "labelColor": _solid("#334155"),
                    "fontSize": _lit("9.5D"),
                    "fontFamily": _lit("'Segoe UI'")
                }
            }
        ]
    }

def create_clustered_column_chart(vis_id, x, y, width, height, cat_entity, cat_prop, val_entity, val_prop, series_entity=None, series_prop=None, title_text=None, subtitle_text=None, primary_color="#0D9488"):
    query_state = {
        "Category": {
            "projections": [
                {
                    "field": {
                        "Column": {
                            "Expression": {"SourceRef": {"Entity": cat_entity}},
                            "Property": cat_prop
                        }
                    },
                    "queryRef": f"{cat_entity}.{cat_prop}"
                }
            ]
        },
        "Y": {
            "projections": [
                {
                    "field": {
                        "Measure": {
                            "Expression": {"SourceRef": {"Entity": val_entity}},
                            "Property": val_prop
                        }
                    },
                    "queryRef": f"{val_entity}.{val_prop}"
                }
            ]
        }
    }

    if series_entity and series_prop:
        query_state["Series"] = {
            "projections": [
                {
                    "field": {
                        "Column": {
                            "Expression": {"SourceRef": {"Entity": series_entity}},
                            "Property": series_prop
                        }
                    },
                    "queryRef": f"{series_entity}.{series_prop}"
                }
            ]
        }

    return {
        "$schema": SCHEMA_CONTAINER,
        "name": vis_id,
        "position": {
            "x": x, "y": y, "z": 300,
            "height": height, "width": width,
            "tabOrder": 300
        },
        "visual": {
            "visualType": "clusteredColumnChart",
            "query": {
                "queryState": query_state
            },
            "visualContainerObjects": get_container_styling(title_text, subtitle_text),
            "objects": get_chart_objects(primary_color)
        }
    }

def create_multi_measure_column_chart(vis_id, x, y, width, height, cat_entity, cat_prop, val_items, title_text=None, subtitle_text=None):
    y_projections = []
    for entity, prop in val_items:
        y_projections.append({
            "field": {
                "Measure": {
                    "Expression": {"SourceRef": {"Entity": entity}},
                    "Property": prop
                }
            },
            "queryRef": f"{entity}.{prop}"
        })

    return {
        "$schema": SCHEMA_CONTAINER,
        "name": vis_id,
        "position": {
            "x": x, "y": y, "z": 300,
            "height": height, "width": width,
            "tabOrder": 300
        },
        "visual": {
            "visualType": "clusteredColumnChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Entity": cat_entity}},
                                        "Property": cat_prop
                                    }
                                },
                                "queryRef": f"{cat_entity}.{cat_prop}"
                            }
                        ]
                    },
                    "Y": {
                        "projections": y_projections
                    }
                }
            },
            "visualContainerObjects": get_container_styling(title_text, subtitle_text),
            "objects": {
                "categoryAxis": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "labelColor": _solid("#1E293B"),
                            "fontSize": _lit("10.5D"),
                            "fontFamily": _lit("'Segoe UI Semibold'")
                        }
                    }
                ],
                "valueAxis": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "labelColor": _solid("#64748B"),
                            "fontSize": _lit("9.5D"),
                            "fontFamily": _lit("'Segoe UI'"),
                            "gridlineShow": _lit("true"),
                            "gridlineColor": _solid("#F1F5F9")
                        }
                    }
                ],
                "labels": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid("#0F172A"),
                            "fontSize": _lit("9.5D"),
                            "fontFamily": _lit("'Segoe UI Semibold'"),
                            "labelPosition": _lit("'OutsideEnd'")
                        }
                    }
                ],
                "legend": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "labelColor": _solid("#334155"),
                            "fontSize": _lit("9.5D"),
                            "fontFamily": _lit("'Segoe UI'")
                        }
                    }
                ]
            }
        }
    }

def create_bar_chart(vis_id, x, y, width, height, cat_entity, cat_prop, val_entity, val_prop, title_text=None, subtitle_text=None, primary_color="#0D9488"):
    return {
        "$schema": SCHEMA_CONTAINER,
        "name": vis_id,
        "position": {
            "x": x, "y": y, "z": 300,
            "height": height, "width": width,
            "tabOrder": 300
        },
        "visual": {
            "visualType": "clusteredBarChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Entity": cat_entity}},
                                        "Property": cat_prop
                                    }
                                },
                                "queryRef": f"{cat_entity}.{cat_prop}"
                            }
                        ]
                    },
                    "Y": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Entity": val_entity}},
                                        "Property": val_prop
                                    }
                                },
                                "queryRef": f"{val_entity}.{val_prop}"
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": get_container_styling(title_text, subtitle_text),
            "objects": get_chart_objects(primary_color)
        }
    }

def create_area_chart(vis_id, x, y, width, height, cat_entity, cat_prop, val_entity, val_prop, title_text=None, subtitle_text=None, primary_color="#0D9488"):
    return {
        "$schema": SCHEMA_CONTAINER,
        "name": vis_id,
        "position": {
            "x": x, "y": y, "z": 400,
            "height": height, "width": width,
            "tabOrder": 400
        },
        "visual": {
            "visualType": "areaChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Entity": cat_entity}},
                                        "Property": cat_prop
                                    }
                                },
                                "queryRef": f"{cat_entity}.{cat_prop}"
                            }
                        ]
                    },
                    "Y": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Entity": val_entity}},
                                        "Property": val_prop
                                    }
                                },
                                "queryRef": f"{val_entity}.{val_prop}"
                            }
                        ]
                    }
                }
            },
            "visualContainerObjects": get_container_styling(title_text, subtitle_text),
            "objects": {
                "categoryAxis": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "labelColor": _solid("#1E293B"),
                            "fontSize": _lit("10.5D"),
                            "fontFamily": _lit("'Segoe UI Semibold'")
                        }
                    }
                ],
                "valueAxis": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "labelColor": _solid("#64748B"),
                            "fontSize": _lit("9.5D"),
                            "fontFamily": _lit("'Segoe UI'"),
                            "gridlineShow": _lit("true"),
                            "gridlineColor": _solid("#F1F5F9")
                        }
                    }
                ],
                "labels": [
                    {
                        "properties": {
                            "show": _lit("true"),
                            "color": _solid("#0F172A"),
                            "fontSize": _lit("9.5D"),
                            "fontFamily": _lit("'Segoe UI Semibold'")
                        }
                    }
                ]
            }
        }
    }

def create_table_visual(vis_id, x, y, width, height, entity, col_specs, title_text=None, subtitle_text=None):
    """
    col_specs: list of tuples: (col_property, display_name, format_str)
    """
    projections = []
    for prop, disp, fmt in col_specs:
        proj = {
            "field": {
                "Column": {
                    "Expression": {"SourceRef": {"Entity": entity}},
                    "Property": prop
                }
            },
            "queryRef": f"{entity}.{prop}"
        }
        if disp:
            proj["displayName"] = disp
        if fmt:
            proj["format"] = fmt
        projections.append(proj)

    return {
        "$schema": SCHEMA_CONTAINER,
        "name": vis_id,
        "position": {
            "x": x, "y": y, "z": 500,
            "height": height, "width": width,
            "tabOrder": 500
        },
        "visual": {
            "visualType": "tableEx",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": projections
                    }
                }
            },
            "visualContainerObjects": get_container_styling(title_text, subtitle_text),
            "objects": {
                "columnHeaders": [
                    {
                        "properties": {
                            "fontSize": _lit("12D"),
                            "fontFamily": _lit("'Segoe UI Semibold'"),
                            "fontColor": _solid("#FFFFFF"),
                            "backColor": _solid("#0F172A"),
                            "autoSizeColumnWidth": _lit("true"),
                            "wordWrap": _lit("true")
                        }
                    }
                ],
                "values": [
                    {
                        "properties": {
                            "fontSize": _lit("11D"),
                            "fontFamily": _lit("'Segoe UI'"),
                            "fontColorPrimary": _solid("#0F172A"),
                            "backColorPrimary": _solid("#FFFFFF"),
                            "backColorSecondary": _solid("#F8FAFC"),
                            "wordWrap": _lit("true")
                        }
                    }
                ],
                "grid": [
                    {
                        "properties": {
                            "gridHorizontal": _lit("true"),
                            "gridHorizontalColor": _solid("#E2E8F0"),
                            "gridVertical": _lit("true"),
                            "gridVerticalColor": _solid("#F1F5F9"),
                            "rowPadding": _lit("10D"),
                            "outlineColor": _solid("#0F172A"),
                            "outlineWeight": _lit("1D")
                        }
                    }
                ],
                "total": [
                    {
                        "properties": {
                            "totals": _lit("false")
                        }
                    }
                ]
            }
        }
    }

def save_visual(page_id, vis_dict):
    vis_name = vis_dict["name"]
    vis_dir = os.path.join(PAGES_DIR, page_id, "visuals", vis_name)
    os.makedirs(vis_dir, exist_ok=True)
    file_path = os.path.join(vis_dir, "visual.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(vis_dict, f, indent=2, ensure_ascii=False)

def build_all_pbir_dashboards():
    print("[*] Bắt đầu tạo 4 trang Executive Dashboards chuẩn PBIR v2...")

    # Dọn dẹp thư mục pages cũ
    if os.path.exists(PAGES_DIR):
        for item in os.listdir(PAGES_DIR):
            item_path = os.path.join(PAGES_DIR, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif item.endswith(".json"):
                os.remove(item_path)

    os.makedirs(PAGES_DIR, exist_ok=True)

    pages = [
        {"id": "p1_funnel", "name": "1. Tổng quan & Động học phễu"},
        {"id": "p2_gmm", "name": "2. Rào cản vi mô & 5 Cụm GMM"},
        {"id": "p3_survival", "name": "3. Sống còn Kaplan-Meier & Causal Uplift"},
        {"id": "p4_whatif", "name": "4. Tối ưu What-If & Đề xuất hành động"},
    ]

    # Ghi pages.json
    pages_meta = {
        "$schema": SCHEMA_PAGES_META,
        "pageOrder": [p["id"] for p in pages],
        "activePageName": pages[0]["id"]
    }
    with open(os.path.join(PAGES_DIR, "pages.json"), "w", encoding="utf-8") as f:
        json.dump(pages_meta, f, indent=2)

    page_bg_obj = {
        "background": [
            {
                "properties": {
                    "color": _solid("#F8FAFC"),
                    "transparency": _lit("0D")
                }
            }
        ]
    }

    # ========================================================
    # TRANG 1: TỔNG QUAN ĐIỀU HÀNH & ĐỘNG HỌC PHỄU CHUYỂN ĐỔI
    # ========================================================
    p1_dir = os.path.join(PAGES_DIR, "p1_funnel")
    os.makedirs(p1_dir, exist_ok=True)
    p1_cfg = {
        "$schema": SCHEMA_PAGE,
        "name": "p1_funnel",
        "displayName": "1. Tổng quan & Động học phễu",
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920,
        "objects": page_bg_obj
    }
    with open(os.path.join(p1_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump(p1_cfg, f, indent=2)

    # 1. Top Executive Banner (Y: 15, H: 75)
    save_visual("p1_funnel", create_banner_visual(
        "p1_banner", 20, 15, 1880, 75,
        "Banner Page 1",
        "Khung phân tích chuyển đổi phễu 4 giai đoạn, tỷ lệ CVR tự nhiên và quy mô khách hàng"
    ))

    # 2. 4 KPI Cards (Y: 105, H: 110, W: 455)
    save_visual("p1_funnel", create_card_visual(
        "p1_kpi_cust", 20, 105, 455, 110,
        "fact_customer_decisions", "Total Customers",
        "TỔNG QUY MÔ KHÁCH HÀNG",
        "997k phiên truy cập / 249k giao dịch toàn sàn",
        "#0F172A"
    ))
    save_visual("p1_funnel", create_card_visual(
        "p1_kpi_aban", 495, 105, 455, 110,
        "fact_customer_decisions", "Avg Abandonment Rate",
        "TỶ LỆ BỎ GIỎ TOÀN CẦU (BAYMARD)",
        "Benchmark thương mại điện tử quốc tế: ~70%",
        "#E11D48"
    ))
    save_visual("p1_funnel", create_card_visual(
        "p1_kpi_profit", 970, 105, 455, 110,
        "fact_customer_decisions", "Max Holdout Profit",
        "LỢI NHUẬN THU HỒI CỰC ĐẠI (τ* = 0.07)",
        "Vượt trội +$41,200 so với ngưỡng mặc định τ=0.50",
        "#059669"
    ))
    save_visual("p1_funnel", create_card_visual(
        "p1_kpi_cac", 1445, 105, 455, 110,
        "fact_customer_decisions", "CAC Savings Pct",
        "TIẾT KIỆM NGÂN SÁCH TIẾP CẬN CAC",
        "Nhắm chọn Top 20% Lift@K thay vì tiếp cận đại trà",
        "#4F46E5"
    ))

    # 3. 4 Main Visuals Grid
    # Top-Left: Phễu chuyển đổi 4 giai đoạn
    save_visual("p1_funnel", create_bar_chart(
        "p1_chart_funnel", 20, 230, 925, 400,
        "dim_funnel_stages", "stage_name",
        "fact_customer_decisions", "Funnel Users Count",
        title_text="1. Phễu Chuyển Đổi Toàn Sàn 4 Giai Đoạn (Từ Phiên Đến Mua Hàng)",
        subtitle_text="Động học quy mô người dùng qua 4 tầng phễu (Phiên → Xem SP → Thêm giỏ → Mua)",
        primary_color="#0D9488"
    ))

    # Top-Right: Bảng động học chi tiết tỷ lệ chuyển đổi & rơi rụng
    save_visual("p1_funnel", create_table_visual(
        "p1_tbl_funnel", 975, 230, 925, 400,
        "dim_funnel_stages",
        [
            ("stage_order", "Thứ Tự", "0"),
            ("stage_name", "Giai Đoạn Phễu", None),
            ("stage_users_count", "Quy Mô Phiên (Users)", "#,##0"),
            ("conversion_rate_pct", "Tỷ Lệ Chuyển Đổi CVR", '0.0"%"'),
            ("drop_off_rate_pct", "Tỷ Lệ Rơi Rụng (Drop-off)", '0.0"%"')
        ],
        title_text="2. Động Học Tỷ Lệ Chuyển Đổi & Rơi Rụng (Drop-off) Từng Tầng Phễu",
        subtitle_text="Bảng chỉ số tổn thất lưu lượng chi tiết giữa các tầng chuyển hóa"
    ))

    # Bottom-Left: Tỷ lệ chuyển đổi theo Hạng hội viên & Nhóm tuổi
    save_visual("p1_funnel", create_clustered_column_chart(
        "p1_chart_age_tier", 20, 645, 925, 410,
        "dim_customers", "age_group",
        "fact_customer_decisions", "Baseline Conversion Rate",
        series_entity="dim_customers", series_prop="customer_tier",
        title_text="3. Tỷ Lệ Chuyển Đổi (CVR) Theo Nhóm Tuổi & Phân Hạng Hội Viên",
        subtitle_text="Phân tích CVR tự nhiên giữa 4 hạng hội viên (Bronze, Silver, Gold, Platinum)"
    ))

    # Bottom-Right: Phân bổ khách hàng theo quốc gia
    save_visual("p1_funnel", create_bar_chart(
        "p1_chart_country", 975, 645, 925, 410,
        "dim_customers", "country",
        "fact_customer_decisions", "Total Customers",
        title_text="4. Quy Mô Phân Bổ Khách Hàng Theo Thị Trường Quốc Gia Trọng Điểm",
        subtitle_text="Quy mô khách hàng tích lũy tại các thị trường trọng điểm (US, UK, CA, IN, DE)",
        primary_color="#4F46E5"
    ))

    # ========================================================
    # TRANG 2: RÀO CẢN HÀNH VI VI MÔ & PHÂN CỤM GMM (k*=5)
    # ========================================================
    p2_dir = os.path.join(PAGES_DIR, "p2_gmm")
    os.makedirs(p2_dir, exist_ok=True)
    p2_cfg = {
        "$schema": SCHEMA_PAGE,
        "name": "p2_gmm",
        "displayName": "2. Rào cản vi mô & 5 Cụm GMM",
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920,
        "objects": page_bg_obj
    }
    with open(os.path.join(p2_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump(p2_cfg, f, indent=2)

    # 1. Top Executive Banner
    save_visual("p2_gmm", create_banner_visual(
        "p2_banner", 20, 15, 1880, 75,
        "Banner Page 2",
        "Chẩn đoán rào cản cước phí Overnight, chỉ số đắn đo giỏ hàng và hồ sơ 5 phân khúc k*=5"
    ))

    # 2. 4 KPI Cards (Y: 105, H: 110, W: 455)
    save_visual("p2_gmm", create_card_visual(
        "p2_kpi_share", 20, 105, 455, 110,
        "fact_customer_decisions", "Hesitators Population Share",
        "CỤM 2: CART HESITATORS (TRỌNG TÂM)",
        "50,077 khách hàng nhạy cảm cước phí vận chuyển",
        "#E11D48"
    ))
    save_visual("p2_gmm", create_card_visual(
        "p2_kpi_index", 495, 105, 455, 110,
        "fact_customer_decisions", "Avg Hesitation Index",
        "CHỈ SỐ ĐẮN ĐO GIỎ HÀNG (HESITATION)",
        "Thời gian dừng lại cân nhắc giá (giây/mặt hàng)",
        "#0D9488"
    ))
    save_visual("p2_gmm", create_card_visual(
        "p2_kpi_overnight", 970, 105, 455, 110,
        "fact_customer_decisions", "Overnight Ratio",
        "TỶ LỆ CHỌN GIAO HỎA TỐC OVERNIGHT",
        "Ma sát chi phí cước hỏa tốc gây bỏ giỏ hàng loạt",
        "#D97706"
    ))
    save_visual("p2_gmm", create_card_visual(
        "p2_kpi_aban", 1445, 105, 455, 110,
        "fact_customer_decisions", "Cluster 2 Abandonment",
        "MỨC ĐỘ BỎ GIỎ BÌNH QUÂN CỤM 2",
        "Thang đo độ nghiêm trọng từ bỏ giỏ hàng (1.0 - 5.0)",
        "#0F172A"
    ))

    # 3. Visuals Grid
    # Top-Left: So sánh AOV theo 5 Cụm GMM
    save_visual("p2_gmm", create_clustered_column_chart(
        "p2_chart_aov", 20, 230, 925, 400,
        "tbl_ch3_gmm_cluster_profiles", "persona_name",
        "tbl_ch3_gmm_cluster_profiles", "GMM AOV",
        title_text="1. So Sánh Giá Trị Đơn Hàng Trung Bình (AOV USD) Giữa 5 Cụm GMM",
        subtitle_text="Đo lường mức chi tiêu đơn hàng tiềm năng giữa các phân khúc RFM-E",
        primary_color="#0D9488"
    ))

    # Top-Right: Mức độ bỏ giỏ bình quân theo 5 Cụm
    save_visual("p2_gmm", create_clustered_column_chart(
        "p2_chart_ship", 975, 230, 925, 400,
        "tbl_ch3_gmm_cluster_profiles", "persona_name",
        "tbl_ch3_gmm_cluster_profiles", "GMM Cart Abandonment",
        title_text="2. Mức Độ Từ Bỏ Giỏ Hàng Bình Quân Theo 5 Cụm Hành Vi GMM",
        subtitle_text="Điểm số mức độ nghiêm trọng bỏ giỏ (Cart Abandonment Severity 1.0 - 5.0)",
        primary_color="#E11D48"
    ))

    # Bottom Full Width: Bảng Master Profile 5 Cụm GMM
    save_visual("p2_gmm", create_table_visual(
        "p2_tbl_gmm", 20, 645, 1880, 410,
        "tbl_ch3_gmm_cluster_profiles",
        [
            ("cluster_id", "Mã Cụm", "0"),
            ("persona_name", "Chân Dung Khách Hàng GMM (k*=5)", None),
            ("customer_count", "Quy Mô (Khách)", "#,##0"),
            ("pct_population", "Tỷ Trọng Dân Số", '0.00"%"'),
            ("mean_monetary", "Chi Tiêu AOV ($)", "$#,##0.00"),
            ("mean_recency", "Độ Trễ Recency (Ngày)", "#,##0.0"),
            ("mean_frequency", "Tần Suất Mua (Đơn)", "#,##0.0"),
            ("mean_cart_additions", "Lượt Thêm Giỏ", "#,##0.0"),
            ("mean_abandonment_severity", "Mức Bỏ Giỏ (1-5)", "#,##0.0"),
            ("conversion_rate", "Tỷ Lệ Mua CVR", '0.00"%"')
        ],
        title_text="3. Bảng Hồ Sơ Chân Dung Hành Vi Và Tiềm Năng Kinh Tế Toàn Diện 5 Phân Khúc GMM (k*=5)",
        subtitle_text="Ma trận 10 chiều chỉ số hành vi, tài chính và tỷ lệ chuyển đổi mua hàng của toàn bộ 200,000 khách hàng"
    ))

    # ========================================================
    # TRANG 3: SỐNG CÒN KAPLAN-MEIER & SUY LUẬN NHÂN QUẢ UPLIFT
    # ========================================================
    p3_dir = os.path.join(PAGES_DIR, "p3_survival")
    os.makedirs(p3_dir, exist_ok=True)
    p3_cfg = {
        "$schema": SCHEMA_PAGE,
        "name": "p3_survival",
        "displayName": "3. Sống còn Kaplan-Meier & Causal Uplift",
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920,
        "objects": page_bg_obj
    }
    with open(os.path.join(p3_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump(p3_cfg, f, indent=2)

    # 1. Top Executive Banner
    save_visual("p3_survival", create_banner_visual(
        "p3_banner", 20, 15, 1880, 75,
        "Banner Page 3",
        "Phân tích sống còn phân rã giỏ hàng Kaplan-Meier và ma trận can thiệp cá thể hóa Uplift"
    ))

    # 2. 4 KPI Cards (Y: 105, H: 110, W: 455)
    save_visual("p3_survival", create_card_visual(
        "p3_kpi_win", 20, 105, 455, 110,
        "fact_customer_decisions", "Critical Decay Window",
        "THỜI ĐIỂM VÀNG CAN THIỆP SỐNG CÒN",
        "Hàm phân rã Kaplan-Meier: Rơi rụng mạnh sau 7 ngày",
        "#E11D48"
    ))
    save_visual("p3_survival", create_card_visual(
        "p3_kpi_persuade", 495, 105, 455, 110,
        "fact_customer_decisions", "Persuadables Pct",
        "TỶ TRỌNG NHÓM PERSUADABLES",
        "11,200 khách hàng tiếp thị can thiệp sinh lời thực tế",
        "#059669"
    ))
    save_visual("p3_survival", create_card_visual(
        "p3_kpi_budget", 970, 105, 455, 110,
        "fact_customer_decisions", "Saved Budget",
        "NGÂN SÁCH TIẾT KIỆM (SURE THINGS)",
        "Bảo toàn chi phí voucher bằng cách loại bỏ nhóm tự mua",
        "#0D9488"
    ))
    save_visual("p3_survival", create_card_visual(
        "p3_kpi_tau", 1445, 105, 455, 110,
        "fact_customer_decisions", "Avg Uplift Tau",
        "UPLIFT THUẦN (NET INCREMENTAL CATE)",
        "Mức gia tăng chuyển đổi thực tế do can thiệp mang lại",
        "#4F46E5"
    ))

    # 3. Visuals Grid
    # Top-Left: Sống còn Kaplan-Meier theo 4 Phân tầng (7 ngày & 30 ngày)
    save_visual("p3_survival", create_multi_measure_column_chart(
        "p3_chart_km", 20, 230, 925, 400,
        "tbl_ch4_survival_summary", "stratum_name",
        [
            ("fact_customer_decisions", "Survival Prob 7D"),
            ("fact_customer_decisions", "Survival Prob 30D")
        ],
        title_text="1. Xác Suất Phục Hồi Giỏ Hàng Kaplan-Meier Tại Mốc 7 Ngày & 30 Ngày",
        subtitle_text="So sánh xác suất duy trì ý định mua S(t) theo 4 phương thức giao hàng"
    ))

    # Top-Right: CoxPH Hazard Ratios (Rào cản ma sát)
    save_visual("p3_survival", create_bar_chart(
        "p3_chart_coxph", 975, 230, 925, 400,
        "tbl_ch4_coxph_hazard_ratios", "covariate",
        "fact_customer_decisions", "Hazard Ratio Score",
        title_text="2. Hồi Quy Tỷ Số Nguy Cơ CoxPH (Hazard Ratio > 1 Làm Tăng Nguy Cơ Bỏ Giỏ)",
        subtitle_text="Tỷ số rủi ro Hazard Ratio của các yếu tố ma sát thanh toán và giao hàng",
        primary_color="#E11D48"
    ))

    # Bottom Full Width: Bảng Phân Bổ 4 Nhóm Tiếp Thị Uplift CATE
    save_visual("p3_survival", create_table_visual(
        "p3_tbl_uplift", 20, 645, 1880, 410,
        "tbl_ch4_uplift_segments_summary",
        [
            ("uplift_segment", "Phân Nhóm Tiếp Thị Uplift CATE", None),
            ("customer_count", "Quy Mô (Khách)", "#,##0"),
            ("pct_population", "Tỷ Trọng Dân Số", '0.00"%"'),
            ("mean_uplift_score", "Điểm Uplift Thuần (CATE)", "+0.00%;-0.00%;0.00%"),
            ("control_conversion_rate", "CVR Đối Chứng (Control)", '0.00"%"'),
            ("treatment_conversion_rate", "CVR Can Thiệp (Treatment)", '0.00"%"'),
            ("net_incremental_orders", "Đơn Tăng Thêm Thuần", "#,##0"),
            ("business_recommendation", "Đề Xuất Hành Động Can Thiệp Tác Chiến", None)
        ],
        title_text="3. Ma Trận Phân Bổ 4 Nhóm Tiếp Thị Nhân Quả Uplift CATE (32,000 Khách Hàng Kiểm Thử)",
        subtitle_text="Phân định 4 nhóm đối tượng: Persuadables (ưu tiên 1), Sure Things (cấm voucher), Lost Causes (loại bỏ), Sleeping Dogs (không can thiệp)"
    ))

    # ========================================================
    # TRANG 4: TỐI ƯU HÓA LỢI NHUẬN WHAT-IF & MA TRẬN HÀNH ĐỘNG
    # ========================================================
    p4_dir = os.path.join(PAGES_DIR, "p4_whatif")
    os.makedirs(p4_dir, exist_ok=True)
    p4_cfg = {
        "$schema": SCHEMA_PAGE,
        "name": "p4_whatif",
        "displayName": "4. Tối ưu What-If & Đề xuất hành động",
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920,
        "objects": page_bg_obj
    }
    with open(os.path.join(p4_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump(p4_cfg, f, indent=2)

    # 1. Top Executive Banner
    save_visual("p4_whatif", create_banner_visual(
        "p4_banner", 20, 15, 1880, 75,
        "Banner Page 4",
        "Mô phỏng đường cong lợi nhuận What-If theo ngưỡng phân loại và hiệu năng 10-Decile Lift"
    ))

    # 2. 4 KPI Cards (Y: 105, H: 110, W: 455)
    save_visual("p4_whatif", create_card_visual(
        "p4_kpi_tau", 20, 105, 455, 110,
        "fact_customer_decisions", "Optimal Threshold Tau",
        "NGƯỠNG QUYẾT ĐỊNH KINH TẾ TỐI ƯU",
        "Điểm cực đại hóa lợi nhuận tài chính ròng τ* = 0.07",
        "#059669"
    ))
    save_visual("p4_whatif", create_card_visual(
        "p4_kpi_profit", 495, 105, 455, 110,
        "fact_customer_decisions", "Max Net Profit USD",
        "LỢI NHUẬN RÒNG CỰC ĐẠI (HOLDOUT)",
        "Đạt được trên tập kiểm định 32,000 khách hàng",
        "#0D9488"
    ))
    save_visual("p4_whatif", create_card_visual(
        "p4_kpi_delta", 970, 105, 455, 110,
        "fact_customer_decisions", "Profit Delta vs Default",
        "THẶNG DƯ TÀI CHÍNH BỔ SUNG (+55.1%)",
        "Tăng thêm +$41,200 so với việc chọn ngưỡng mặc định 0.50",
        "#4F46E5"
    ))
    save_visual("p4_whatif", create_card_visual(
        "p4_kpi_lift", 1445, 105, 455, 110,
        "fact_customer_decisions", "Decile 1 Lift",
        "HỆ SỐ NÂNG CHUYỂN ĐỔI (DECILE 1)",
        "Top 10% khách hàng đạt tỷ lệ chuyển đổi gấp 1.61 lần baseline",
        "#D97706"
    ))

    # 3. Visuals Grid
    # Top-Left: Đường cong lợi nhuận What-If (AreaChart)
    save_visual("p4_whatif", create_area_chart(
        "p4_chart_profit", 20, 230, 925, 400,
        "dim_threshold_simulation", "threshold",
        "fact_customer_decisions", "Expected Net Profit",
        title_text="1. Đường Cong Mô Phỏng Tối Ưu Hóa Lợi Nhuận Ròng What-If Theo Ngưỡng Xác Suất τ",
        subtitle_text="Đỉnh lợi nhuận cực đại $115,918 tại ngưỡng τ* = 0.07 (vượt trội +$41,200 so với τ=0.50)",
        primary_color="#0D9488"
    ))

    # Top-Right: Biểu đồ 10-Decile Lift@K (ColumnChart)
    save_visual("p4_whatif", create_clustered_column_chart(
        "p4_chart_decile", 975, 230, 925, 400,
        "tbl_ch5_decile_lift_profit", "decile",
        "fact_customer_decisions", "Decile Lift Score",
        title_text="2. Hiệu Năng Phân Bổ 10-Decile Lift@K & Tỷ Lệ Phản Ứng Khách Hàng",
        subtitle_text="Xếp hạng phân vị từ D1 (Lift 1.61x, CVR 32.78%) giảm dần đến D10 (Lift 0.52x)",
        primary_color="#4F46E5"
    ))

    # Bottom Full Width: Bảng Ma Trận 4 Gói Hành Động Kinh Doanh Chi Tiết
    save_visual("p4_whatif", create_table_visual(
        "p4_tbl_action_matrix", 20, 645, 1880, 410,
        "tbl_ch5_business_action_matrix",
        [
            ("strategy_id", "Mã Chiến Lược", None),
            ("strategy_name", "Tên Gói Hành Động Đề Xuất", None),
            ("target_segment", "Phân Khúc Mục Tiêu", None),
            ("intervention_action", "Hành Động Can Thiệp Cụ Thể", None),
            ("channel", "Kênh Triển Khai", None),
            ("optimal_threshold", "Ngưỡng Quyết Định (τ*)", None),
            ("potential_risks", "Rủi Ro Tiềm Ẩn", None),
            ("mitigation_plan", "Kế Hoạch Giảm Thiểu Rủi Ro", None),
            ("target_kpi", "Chỉ Số Đo Lường Mục Tiêu (KPI)", None)
        ],
        title_text="3. Ma Trận 4 Gói Đề Xuất Hành Động Kinh Doanh Chi Tiết (ACT-01 → ACT-04 Chuyển Hóa Thặng Dư)",
        subtitle_text="Kế hoạch tác chiến toàn diện: Miễn phí vận chuyển linh hoạt, Flash voucher đếm ngược, Tái kích hoạt email, Chăm sóc đặc quyền VIP"
    ))

    print("[+] HOÀN THÀNH TẠO 100% EXECUTIVE VISUALS CHO CẢ 4 TRANG BÁO CÁO TRONG PBIR!")

if __name__ == "__main__":
    build_all_pbir_dashboards()
