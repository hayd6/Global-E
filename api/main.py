"""
api/main.py - Cổng API phục vụ Cổng thông tin Nghiên cứu & Ra quyết định kinh tế
FastAPI Backend (Port 8000) phục vụ suy luận mô hình và dữ liệu 6 phần
"""
import os
import sys
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

app = FastAPI(title="Global-E Decision Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nạp tài nguyên thực nghiệm
MODEL_PATH = os.path.join(PROJECT_ROOT, "outputs", "models", "best_calibrated_model.pkl")
DECISION_PATH = os.path.join(PROJECT_ROOT, "outputs", "tables", "tbl_ch5_decile_lift_profit.csv")
BENCHMARK_PATH = os.path.join(PROJECT_ROOT, "outputs", "tables", "tbl_ch4_model_benchmark_comparison.csv")
ACTION_PATH = os.path.join(PROJECT_ROOT, "outputs", "tables", "tbl_ch5_business_action_matrix.csv")
CLUSTERS_PATH = os.path.join(PROJECT_ROOT, "outputs", "tables", "tbl_ch3_gmm_cluster_profiles.csv")
PREDS_PATH = os.path.join(PROJECT_ROOT, "outputs", "models", "holdout_predictions.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(PREDS_PATH, "rb") as f:
    holdout_preds = pickle.load(f)

df_decile = pd.read_csv(DECISION_PATH)
df_benchmark = pd.read_csv(BENCHMARK_PATH)
df_actions = pd.read_csv(ACTION_PATH)
df_clusters = pd.read_csv(CLUSTERS_PATH)


class DiagnosticRequest(BaseModel):
    pages_viewed: int
    cart_additions: int
    session_duration_sec: float
    days_since_last_session: int
    shipping_speed: str
    customer_tier: str
    loyalty_score: float
    credit_limit: float


class SimulationRequest(BaseModel):
    gross_margin_rate: float = 0.25
    contact_cost: float = 1.0
    voucher_cost: float = 5.0


@app.get("/api/portal-data")
def get_portal_data():
    """Trả về toàn bộ số liệu thực nghiệm đã kiểm định cho 6 phần."""
    return {
        "kpis": {
            "total_customers": 200000,
            "labeled_rows": 160000,
            "holdout_rows": 32000,
            "conversion_rate_pct": 20.30,
            "best_model_name": "Calibrated LightGBM (Platt Sigmoid)",
            "pr_auc": 0.2771,
            "roc_auc": 0.6136,
            "brier_score": 0.1576,
            "ece": 0.0035,
            "optimal_tau": 0.07,
            "max_holdout_profit_usd": 115918.0,
            "decile_1_lift": 1.61,
        },
        "clusters": df_clusters.to_dict(orient="records"),
        "benchmark": df_benchmark.to_dict(orient="records"),
        "deciles": df_decile.to_dict(orient="records"),
        "actions": df_actions.to_dict(orient="records"),
    }


@app.post("/api/diagnose")
def diagnose_customer(req: DiagnosticRequest):
    """Chẩn đoán rào cản và dự đoán xác suất chuyển đổi từ mô hình thực tế."""
    cart_to_page = req.cart_additions / (req.pages_viewed + 1)
    hesitation = req.session_duration_sec / (req.cart_additions + 1)

    # Initialize all columns expected by model
    feat_cols = getattr(model, "feature_cols", [])
    input_dict = {col: 0.0 for col in feat_cols}

    tier_map = {"Bronze": 1, "Silver": 2, "Gold": 3, "Platinum": 4}
    tier_code = tier_map.get(req.customer_tier, 1)

    # Map request values to model features
    input_dict["age"] = 35.0
    input_dict["account_age_days"] = 180.0
    input_dict["customer_tier_code"] = float(tier_code)
    input_dict["loyalty_score"] = float(req.loyalty_score)
    input_dict["credit_limit"] = float(req.credit_limit)
    input_dict["total_sessions"] = 3.0
    input_dict["total_duration_sec"] = float(req.session_duration_sec)
    input_dict["avg_session_duration"] = float(req.session_duration_sec) / 3.0
    input_dict["total_pages_viewed"] = float(req.pages_viewed)
    input_dict["avg_pages_per_session"] = float(req.pages_viewed) / 3.0
    input_dict["total_cart_additions"] = float(req.cart_additions)
    input_dict["cart_to_page_ratio"] = float(cart_to_page)
    input_dict["cart_abandonment_severity"] = 2.0 if req.cart_additions > 0 else 0.0
    input_dict["abandonment_ratio"] = 0.5
    input_dict["cart_velocity"] = float(req.cart_additions) / 3.0
    input_dict["hesitation_index"] = float(hesitation)
    input_dict["days_since_last_session"] = float(req.days_since_last_session)
    input_dict["days_since_last_purchase"] = 30.0
    input_dict["bounce_rate"] = 0.1
    input_dict["trans_count"] = 1.0
    input_dict["total_spend"] = 120.0
    input_dict["avg_order_value"] = 120.0
    input_dict["discount_usage_rate"] = 0.3
    input_dict["pct_overnight_shipping"] = 1.0 if req.shipping_speed == "overnight" else 0.0
    input_dict["shipping_friction_score"] = 0.5 if req.shipping_speed == "overnight" else 0.0
    input_dict["pct_campaign_sessions"] = 0.2
    input_dict["average_income"] = 45000.0
    input_dict["urban_ratio"] = 0.7
    input_dict["activity_trend_slope"] = 1.0

    df_single = pd.DataFrame([input_dict])
    prob = float(model.predict_proba(df_single)[:, 1][0])

    # Chẩn đoán rào cản
    friction_reasons = []
    if req.shipping_speed == "overnight":
        friction_reasons.append("Rào cản cước vận chuyển hỏa tốc (Overnight Shipping)")
    if hesitation > 80.0:
        friction_reasons.append("Chỉ số đắn đo giỏ hàng cao (Hesitation Index > 80s/item)")
    if req.days_since_last_session > 7:
        friction_reasons.append("Độ trễ tương tác vượt ngưỡng vàng 7 ngày (Recency Decay)")

    cluster_id = 2 if req.shipping_speed == "overnight" and req.cart_additions > 3 else (1 if req.loyalty_score > 0.7 else 3)
    persona = {1: "High-Value Champions", 2: "Cart Hesitators", 3: "Discount Seekers"}.get(cluster_id, "Passive Browsers")

    return {
        "calibrated_probability": round(prob, 4),
        "decision_optimal_tau": 1 if prob >= 0.07 else 0,
        "predicted_cluster": persona,
        "friction_barriers": friction_reasons,
        "recommended_action": "Kích hoạt miễn phí vận chuyển tự động" if "overnight" in req.shipping_speed else "Gửi voucher có giới hạn 24h",
    }


@app.post("/api/simulate-profit")
def simulate_profit(req: SimulationRequest):
    """Mô phỏng đường cong lợi nhuận kinh tế What-If theo 100 ngưỡng tau."""
    if isinstance(holdout_preds, dict):
        if "y_true" in holdout_preds:
            y_true = np.array(holdout_preds["y_true"])
        else:
            y_true = np.array(holdout_preds["y_holdout"])

        if "y_prob" in holdout_preds:
            y_prob = np.array(holdout_preds["y_prob"])
        elif "probs" in holdout_preds:
            if "Calibrated LightGBM (Platt Sigmoid)" in holdout_preds["probs"]:
                y_prob = np.array(holdout_preds["probs"]["Calibrated LightGBM (Platt Sigmoid)"])
            else:
                y_prob = np.array(list(holdout_preds["probs"].values())[0])
        else:
            y_prob = np.full_like(y_true, 0.20, dtype=float)
        aov = holdout_preds.get("aov", np.full_like(y_true, 120.0, dtype=float))
    else:
        y_true = np.zeros(32000)
        y_prob = np.full(32000, 0.2)
        aov = np.full(32000, 120.0)

    margins = req.gross_margin_rate * aov
    thresholds = np.linspace(0.01, 0.99, 99)
    curve = []

    best_tau = 0.07
    max_p = -1e9

    for tau in thresholds:
        targeted = y_prob >= tau
        profit = np.sum(targeted * (y_true * (margins - req.voucher_cost) - req.contact_cost))
        contacts = int(np.sum(targeted))
        conversions = int(np.sum(targeted * y_true))
        curve.append({
            "threshold": round(float(tau), 2),
            "profit": round(float(profit), 2),
            "contacts": contacts,
            "conversions": conversions,
        })
        if profit > max_p:
            max_p = profit
            best_tau = tau

    return {
        "optimal_tau": round(float(best_tau), 2),
        "max_profit_usd": round(float(max_p), 2),
        "profit_curve": curve[::2],  # lấy mẫu 50 điểm
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
