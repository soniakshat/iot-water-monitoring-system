from .models import WaterQualityData
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import CCA
import pandas as pd
import numpy as np
import anomaly_queue as aq  # Import the shared queue


def get_latest_data():
    data = WaterQualityData.objects.order_by('-timestamp')[:1000]
    return pd.DataFrame(list(data.values()))


def perform_incremental_pca_and_cca():
    df = get_latest_data()

    if len(df) < 600:
        return

    # Separate data into environmental and water quality
    env_data = df[['temperature', 'conductivity', 'oxidation_reduction_potential']].values
    quality_data = df.drop(columns=['timestamp', 'temperature', 'conductivity', 'oxidation_reduction_potential']).values

    # Standardize separately
    scaler_env = StandardScaler()
    scaler_quality = StandardScaler()

    env_data_scaled = scaler_env.fit_transform(env_data)
    quality_data_scaled = scaler_quality.fit_transform(quality_data)

    # Perform Incremental PCA
    ipca_env = IncrementalPCA(n_components=2)
    ipca_quality = IncrementalPCA(n_components=2)

    reduced_env = ipca_env.fit_transform(env_data_scaled)
    reduced_quality = ipca_quality.fit_transform(quality_data_scaled)

    # Perform CCA
    cca = CCA(n_components=2)
    cca.fit(reduced_env, reduced_quality)
    env_c, quality_c = cca.transform(reduced_env, reduced_quality)

    # Analyze canonical correlation
    canonical_corr = np.corrcoef(env_c.T, quality_c.T)[:2, 2:]
    canonical_corr = canonical_corr * 1e16
    min_corr = np.min(np.abs(canonical_corr))
    print(f"The canonical corr value: {min_corr}")

    # Detect anomalies
    if min_corr > 0.005:
        print("Anomaly detected in combined water and environmental data!")
        send_alert_to_sse("Anomaly detected in water quality")


def send_alert_to_sse(message):
    """Send an alert to the SSE queue."""
    anomaly_data = {
        "message": message,
        "timestamp": pd.Timestamp.now().isoformat(),
    }
    aq.add_to_queue(anomaly_data)
    print(f"Anomaly added to SSE queue: {anomaly_data}")
