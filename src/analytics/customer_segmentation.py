"""
src/analytics/customer_segmentation.py
Phân khúc khách hàng hành vi RFM-E bằng K-Means, GMM và HDBSCAN
Tuân thủ: .agy/00_CORE_RULES.md và .agy/02_BEHAVIORAL_SEGMENTATION.md
"""

import os
import sys
import gc
import time
import yaml
import duckdb
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score
import hdbscan

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def load_config():
    with open("configs/base_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_segmentation():
    config = load_config()
    tables_dir = config["paths"]["tables_dir"]
    processed_dir = config["paths"]["processed_data_dir"]
    feature_store_path = config["paths"]["feature_store_path"]

    os.makedirs(tables_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    print("--- Loading RFM-E Features from Parquet ---")
    con = duckdb.connect()
    df = con.execute(f"""
        SELECT 
            customer_id,
            days_since_last_session,
            trans_count,
            total_spend,
            total_sessions,
            cart_abandonment_severity,
            total_cart_additions,
            target
        FROM '{feature_store_path}'
        ORDER BY customer_id
    """).df()
    con.close()

    # 1. Prepare RFM-E feature matrix
    rfme_cols = [
        "days_since_last_session",  # R
        "trans_count",             # F
        "total_spend",             # M
        "total_sessions",          # E
        "cart_abandonment_severity"# C (Cart Friction)
    ]
    X_raw = df[rfme_cols].values
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X_raw)

    metrics_records = []
    # Subsample for fast, stable silhouette scoring on 200,000 records
    np.random.seed(42)
    sample_indices = np.random.choice(len(df), size=10000, replace=False)
    X_sub = X_scaled[sample_indices]

    # 2. K-Means Baseline: Scanning k in [3, 8]
    print("\n--- Running K-Means Baseline (k = 3 to 8) ---")
    for k in range(3, 9):
        t0 = time.time()
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        fit_time = round(time.time() - t0, 2)
        
        sil = round(float(silhouette_score(X_sub, labels[sample_indices])), 4)
        dbi = round(float(davies_bouldin_score(X_sub, labels[sample_indices])), 4)
        print(f"K-Means k={k}: Silhouette={sil}, DBI={dbi}, Time={fit_time}s")

        metrics_records.append({
            "algorithm": "K-Means",
            "k_clusters": k,
            "silhouette_score": sil,
            "davies_bouldin_index": dbi,
            "bic_score": np.nan,
            "outlier_ratio": 0.0,
            "fit_time_sec": fit_time
        })

    # 3. Gaussian Mixture Models (GMM): Scanning k in [3, 8]
    print("\n--- Running Gaussian Mixture Models (k = 3 to 8) ---")
    gmm_models = {}
    gmm_bics = {}
    gmm_aics = {}

    for k in range(3, 9):
        t0 = time.time()
        gmm = GaussianMixture(n_components=k, covariance_type="full", random_state=42, n_init=3)
        gmm.fit(X_scaled)
        fit_time = round(time.time() - t0, 2)
        
        bic = round(float(gmm.bic(X_scaled)), 2)
        aic = round(float(gmm.aic(X_scaled)), 2)
        labels = gmm.predict(X_scaled)
        
        sil = round(float(silhouette_score(X_sub, labels[sample_indices])), 4)
        dbi = round(float(davies_bouldin_score(X_sub, labels[sample_indices])), 4)
        print(f"GMM k={k}: BIC={bic:,.0f}, AIC={aic:,.0f}, Silhouette={sil}, DBI={dbi}, Time={fit_time}s")

        metrics_records.append({
            "algorithm": "GMM",
            "k_clusters": k,
            "silhouette_score": sil,
            "davies_bouldin_index": dbi,
            "bic_score": bic,
            "outlier_ratio": 0.0,
            "fit_time_sec": fit_time
        })
        gmm_models[k] = (gmm, labels)
        gmm_bics[k] = bic
        gmm_aics[k] = aic

    # Save BIC/AIC curves for plot_segmentation.py
    bic_df = pd.DataFrame({
        "k": list(range(3, 9)),
        "bic": [gmm_bics[k] for k in range(3, 9)],
        "aic": [gmm_aics[k] for k in range(3, 9)]
    })
    bic_df.to_csv(os.path.join(tables_dir, "tbl_ch3_gmm_bic_aic_raw.csv"), index=False)

    # 4. HDBSCAN Density-based Clustering
    print("\n--- Running HDBSCAN (Density-based) on Sample ---")
    t0 = time.time()
    clusterer = hdbscan.HDBSCAN(min_cluster_size=500, metric="euclidean", cluster_selection_method="eom")
    # Fit HDBSCAN on 20,000 sample for speed and density stability
    sample_20k = np.random.choice(len(df), size=20000, replace=False)
    hdb_labels = clusterer.fit_predict(X_scaled[sample_20k])
    fit_time_hdb = round(time.time() - t0, 2)
    
    outlier_count = int(np.sum(hdb_labels == -1))
    outlier_ratio = round(outlier_count / len(sample_20k), 4)
    valid_mask = hdb_labels != -1
    num_hdb_clusters = len(np.unique(hdb_labels[valid_mask]))
    
    if num_hdb_clusters > 1:
        sil_hdb = round(float(silhouette_score(X_scaled[sample_20k][valid_mask], hdb_labels[valid_mask])), 4)
        dbi_hdb = round(float(davies_bouldin_score(X_scaled[sample_20k][valid_mask], hdb_labels[valid_mask])), 4)
    else:
        sil_hdb, dbi_hdb = np.nan, np.nan
        
    print(f"HDBSCAN: Clusters={num_hdb_clusters}, Outlier Ratio={outlier_ratio*100:.2f}%, Silhouette={sil_hdb}, DBI={dbi_hdb}, Time={fit_time_hdb}s")

    metrics_records.append({
        "algorithm": "HDBSCAN",
        "k_clusters": num_hdb_clusters,
        "silhouette_score": sil_hdb,
        "davies_bouldin_index": dbi_hdb,
        "bic_score": np.nan,
        "outlier_ratio": outlier_ratio,
        "fit_time_sec": fit_time_hdb
    })

    # Save metrics comparison table
    metrics_df = pd.DataFrame(metrics_records)
    metrics_csv = os.path.join(tables_dir, "tbl_ch3_clustering_metrics_comparison.csv")
    metrics_df.to_csv(metrics_csv, index=False)
    print(f"\nClustering metrics comparison saved to {metrics_csv}")

    # 5. Optimal GMM Persona Profiling (k = 5 as standardized in PRD & Phase 2)
    optimal_k = 5
    best_gmm, best_labels = gmm_models[optimal_k]
    df["cluster_raw"] = best_labels

    # Compute cluster statistics to dynamically identify and name the 5 personas
    profiles = []
    cluster_stats = []
    for cid in range(optimal_k):
        c_df = df[df["cluster_raw"] == cid]
        cnt = len(c_df)
        pct = round(cnt * 100.0 / len(df), 2)
        r_mean = c_df["days_since_last_session"].mean()
        f_mean = c_df["trans_count"].mean()
        m_mean = c_df["total_spend"].mean()
        ses_mean = c_df["total_sessions"].mean()
        cart_mean = c_df["total_cart_additions"].mean()
        ab_mean = c_df["cart_abandonment_severity"].mean()
        
        # Conversion rate on labeled subset
        c_labeled = c_df[c_df["target"].notnull()]
        conv_rate = round(float(c_labeled["target"].mean()) * 100.0, 2) if len(c_labeled) > 0 else 0.0

        cluster_stats.append({
            "raw_id": cid,
            "cnt": cnt,
            "pct": pct,
            "recency": r_mean,
            "frequency": f_mean,
            "monetary": m_mean,
            "sessions": ses_mean,
            "cart_additions": cart_mean,
            "abandonment": ab_mean,
            "conv_rate": conv_rate
        })

    # Map raw cluster IDs to standard 5 business personas:
    # 1. High-Value Champions (High monetary, high frequency, high conversion)
    # 2. Cart Hesitators / Shipping-Sensitive (High cart additions, high abandonment severity)
    # 3. Discount Seekers (Moderate monetary, active transactions)
    # 4. Dormant At-Risk (Highest recency / days since last session)
    # 5. Passive Browsers (High sessions/pages, low spend, low cart additions)
    stat_df = pd.DataFrame(cluster_stats)
    
    # Sort and assign personas deterministically based on empirical criteria
    assigned = {}
    
    # High-Value Champions: highest monetary spend
    champ_id = int(stat_df.sort_values(by="monetary", ascending=False).iloc[0]["raw_id"])
    assigned[champ_id] = (1, "High-Value Champions")
    
    remaining = stat_df[~stat_df["raw_id"].isin(assigned.keys())]
    # Dormant At-Risk: highest recency
    dormant_id = int(remaining.sort_values(by="recency", ascending=False).iloc[0]["raw_id"])
    assigned[dormant_id] = (4, "Dormant At-Risk")
    
    remaining = stat_df[~stat_df["raw_id"].isin(assigned.keys())]
    # Cart Hesitators: highest abandonment severity among remaining
    hesitator_id = int(remaining.sort_values(by="abandonment", ascending=False).iloc[0]["raw_id"])
    assigned[hesitator_id] = (2, "Cart Hesitators / Shipping-Sensitive")
    
    remaining = stat_df[~stat_df["raw_id"].isin(assigned.keys())]
    # Discount Seekers: higher conversion/frequency among remaining
    disc_id = int(remaining.sort_values(by="conv_rate", ascending=False).iloc[0]["raw_id"])
    assigned[disc_id] = (3, "Discount Seekers")
    
    remaining = stat_df[~stat_df["raw_id"].isin(assigned.keys())]
    browser_id = int(remaining.iloc[0]["raw_id"])
    assigned[browser_id] = (5, "Passive Browsers")

    print("\n--- Persona Mapping ---")
    for raw_id, (std_id, name) in assigned.items():
        print(f"Raw Cluster {raw_id} -> Cluster {std_id}: {name}")

    # Build final profile table
    final_profiles = []
    for s in cluster_stats:
        std_id, p_name = assigned[s["raw_id"]]
        final_profiles.append({
            "cluster_id": std_id,
            "persona_name": p_name,
            "customer_count": s["cnt"],
            "pct_population": s["pct"],
            "mean_recency": round(s["recency"], 1),
            "mean_frequency": round(s["frequency"], 1),
            "mean_monetary": round(s["monetary"], 2),
            "mean_cart_additions": round(s["cart_additions"], 1),
            "mean_abandonment_severity": round(s["abandonment"], 1),
            "conversion_rate": s["conv_rate"]
        })

    profiles_df = pd.DataFrame(final_profiles).sort_values("cluster_id")
    profiles_csv = os.path.join(tables_dir, "tbl_ch3_gmm_cluster_profiles.csv")
    profiles_df.to_csv(profiles_csv, index=False)
    print(f"\nGMM Cluster Profiles saved to {profiles_csv}:")
    print(profiles_df.to_string(index=False))

    # Save cluster assignment per customer
    id_map = {raw_id: std_id for raw_id, (std_id, _) in assigned.items()}
    df["gmm_cluster_id"] = df["cluster_raw"].map(id_map).astype(np.int8)

    assignments_path = os.path.join(processed_dir, "customer_cluster_assignments.parquet")
    df[["customer_id", "gmm_cluster_id"]].to_parquet(assignments_path, index=False, compression="snappy")
    print(f"\nSaved cluster assignments to {assignments_path}")

    gc.collect()


if __name__ == "__main__":
    run_segmentation()
