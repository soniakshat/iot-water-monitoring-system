from .models import WaterQualityData
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import CCA
import pandas as pd
import numpy as np
import anomaly_queue as aq
import logging


def get_latest_data():
    data = WaterQualityData.objects.order_by('-timestamp')[:1000]
    return pd.DataFrame(list(data.values()))


# Configure logging
logging.basicConfig(level=logging.INFO)


def perform_incremental_pca_and_cca(env_columns=None, quality_columns=None, min_samples=600):
    # Fetch the latest data
    logging.info("Fetching the latest data...")
    df = get_latest_data()

    if len(df) < min_samples:
        logging.warning(f"Insufficient data for analysis. Required: {min_samples}, Found: {len(df)}")
        return

    # Dynamically set environmental and water quality columns
    if env_columns is None:
        env_columns = ['temperature', 'conductivity', 'oxidation_reduction_potential']
    if quality_columns is None:
        quality_columns = [col for col in df.columns if col not in ['timestamp', 'id'] + env_columns]

    # Check for missing values
    if df[env_columns + quality_columns].isnull().any().any():
        logging.error("Data contains missing values. Please clean the data before analysis.")
        return

    logging.info(f"Environmental parameters: {env_columns}")
    logging.info(f"Water quality parameters: {quality_columns}")

    # Split and standardize the data
    env_data = df[env_columns].values
    quality_data = df[quality_columns].values

    env_data_scaled = StandardScaler().fit_transform(env_data)
    quality_data_scaled = StandardScaler().fit_transform(quality_data)

    # Perform Incremental PCA
    ipca_env = IncrementalPCA(n_components=2)
    ipca_quality = IncrementalPCA(n_components=2)

    reduced_env = ipca_env.fit_transform(env_data_scaled)
    reduced_quality = ipca_quality.fit_transform(quality_data_scaled)

    # Analyze PCA loadings
    env_loadings = pd.DataFrame(ipca_env.components_, columns=env_columns)
    quality_loadings = pd.DataFrame(ipca_quality.components_, columns=quality_columns)
    logging.info(f"Environmental PCA Loadings:\n{env_loadings}")
    logging.info(f"Water Quality PCA Loadings:\n{quality_loadings}")

    # Determine which parameters changed the most (highest absolute loading values)
    most_changed_env = env_loadings.abs().idxmax(axis=1)
    most_changed_quality = quality_loadings.abs().idxmax(axis=1)
    logging.info(f"Parameters changing the most in Environmental PCA: {most_changed_env.tolist()}")
    logging.info(f"Parameters changing the most in Water Quality PCA: {most_changed_quality.tolist()}")

    # Perform CCA
    cca = CCA(n_components=2)
    cca.fit(reduced_env, reduced_quality)
    env_c, quality_c = cca.transform(reduced_env, reduced_quality)

    # Analyze canonical correlations
    canonical_corr_matrix = np.corrcoef(env_c.T, quality_c.T)[:2, 2:]
    canonical_corr = np.abs(canonical_corr_matrix)
    min_corr = np.min(canonical_corr) * 1e16

    logging.info(f"Canonical correlations: {canonical_corr}")
    logging.info(f"Minimum canonical correlation: {min_corr}")

    # Detect anomalies based on correlations
    if min_corr > 2.5:
        logging.warning("Anomaly detected in combined water and environmental data!")
        send_alert_to_sse("Anomaly detected in water quality")
    else:
        logging.info("No anomaly detected.")

    # Return results for further use or visualization
    return {
        "reduced_env": reduced_env,
        "reduced_quality": reduced_quality,
        "canonical_corr": canonical_corr,
        "most_changed_env": most_changed_env.tolist(),
        "most_changed_quality": most_changed_quality.tolist(),
        "pca_env_loadings": env_loadings,
        "pca_quality_loadings": quality_loadings,
    }


def send_alert_to_sse(message):
    """Send an alert to the SSE queue."""
    anomaly_data = {
        "message": message,
        "timestamp": pd.Timestamp.now().isoformat(),
    }
    aq.add_to_queue(anomaly_data)
    print(f"Anomaly added to SSE queue: {anomaly_data}")
