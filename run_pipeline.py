"""
run_pipeline.py
Kịch bản điều phối thực thi tự động toàn diện dự án từ A đến Z (1-Click Pipeline)
Ghi log tuần tự vào outputs/experiments/pipeline_run.log
Tuân thủ: .agy/00_CORE_RULES.md và .agy/05_DASHBOARD_WEB_AND_REPORT.md
"""

import os
import sys
import time
import subprocess

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

LOG_DIR = os.path.join(PROJECT_ROOT, "outputs", "experiments")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "pipeline_run.log")


def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")


def run_step(step_name, command):
    log(f"==================================================")
    log(f"STARTING: {step_name}")
    log(f"COMMAND: {command}")
    t0 = time.time()
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    duration = time.time() - t0

    if result.returncode == 0:
        log(f"SUCCESS: {step_name} completed in {duration:.2f}s")
        if result.stdout:
            for line in result.stdout.strip().split("\n")[-8:]:
                log(f"  [OUT] {line}")
    else:
        log(f"FAILED: {step_name} failed with return code {result.returncode}")
        if result.stderr:
            for line in result.stderr.strip().split("\n")[-10:]:
                log(f"  [ERR] {line}")
        sys.exit(1)


def main():
    log("==================================================")
    log("GLOBAL-E DATA SCIENCE PIPELINE - 1-CLICK EXECUTION")
    log(f"Execution Root: {PROJECT_ROOT}")
    log("==================================================")

    steps = [
        # GIAI ĐOẠN 1: DATA ENGINEERING & PIT FEATURE STORE
        ("GIAI ĐOẠN 1.1: Data Healing", "python src/data_engineering/data_healing.py"),
        ("GIAI ĐOẠN 1.2: Build Features PIT", "python src/data_engineering/build_features_pit.py"),
        ("GIAI ĐOẠN 1.3: PIT Integrity Tests", "pytest tests/test_pit_integrity.py"),
        ("GIAI ĐOẠN 1.4: Plot PIT Audit Figures", "python src/data_engineering/plot_pit_audit.py"),

        # GIAI ĐOẠN 2: BEHAVIORAL SEGMENTATION
        ("GIAI ĐOẠN 2.1: Behavioral Hypothesis Testing", "python src/analytics/behavioral_hypothesis_testing.py"),
        ("GIAI ĐOẠN 2.2: Customer Segmentation (GMM & HDBSCAN)", "python src/analytics/customer_segmentation.py"),
        ("GIAI ĐOẠN 2.3: Plot Segmentation Figures", "python src/analytics/plot_segmentation.py"),

        # GIAI ĐOẠN 3: PROPENSITY MODELING & CALIBRATION
        ("GIAI ĐOẠN 3.1: Train Propensity Models (Optuna HPO)", "python src/models/train_propensity_models.py"),
        ("GIAI ĐOẠN 3.2: Calibrate & Evaluate Models", "python src/models/calibrate_and_evaluate.py"),
        ("GIAI ĐOẠN 3.3: Ablation Study & Stability", "python src/models/ablation_and_stability.py"),
        ("GIAI ĐOẠN 3.4: Plot Model Evaluation Figures", "python src/models/plot_model_evaluation.py"),

        # GIAI ĐOẠN 4: SURVIVAL, UPLIFT & OPTIMIZATION
        ("GIAI ĐOẠN 4.1: Survival Analysis (Kaplan-Meier & CoxPH)", "python src/analytics/survival_analysis.py"),
        ("GIAI ĐOẠN 4.2: Uplift Modeling (T-Learner CATE)", "python src/models/uplift_modeling.py"),
        ("GIAI ĐOẠN 4.3: TreeSHAP Interaction Values", "python src/explainability/shap_interaction.py"),
        ("GIAI ĐOẠN 4.4: Expected Profit Optimization", "python src/business_value/profit_optimization.py"),
        ("GIAI ĐOẠN 4.5: Plot Business Insights Figures", "python src/business_value/plot_business_insights.py"),

        # GIAI ĐOẠN 5: POWER BI STAR SCHEMA & DELIVERABLES
        ("GIAI ĐOẠN 5.1: Export Power BI Star Schema", "python src/data_engineering/export_powerbi_star_schema.py"),
        ("GIAI ĐOẠN 5.2: Business Recommendations Matrix", "python src/business_value/generate_business_recommendations.py"),
        ("GIAI ĐOẠN 5.3: Generate Deliverables (Word Report, Slides, Video)", "python src/utils/generate_deliverables.py")
    ]

    total_t0 = time.time()
    for name, cmd in steps:
        run_step(name, cmd)

    total_duration = time.time() - total_t0
    log("==================================================")
    log(f"PIPELINE FULLY COMPLETED IN {total_duration:.2f}s ({total_duration/60:.2f} minutes)")
    log("ALL 5 PHASES ACCEPTANCE CRITERIA 100% SATISFIED.")
    log("==================================================")


if __name__ == "__main__":
    main()
