import pandas as pd
from .models import WaterQualityData
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import StandardScaler
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import numpy as np
from sklearn.cross_decomposition import CCA

def get_latest_data():
    # Fetch the latest 600 records
    data = WaterQualityData.objects.order_by('-timestamp')[:600]
    return pd.DataFrame(list(data.values()))

def perform_incremental_pca_and_cca():
    df = get_latest_data()
    if len(df) < 600:
        return  # Ensure we have enough data points

    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df.drop(columns=['timestamp']))

    # Separate into environmental and water quality data
    # Environmental data: temperature, conductivity, oxidation_reduction_potential
    env_data = df[['temperature', 'conductivity', 'oxidation_reduction_potential']].values

    # Water quality data: all other fields except timestamp
    quality_data = df.drop(columns=['timestamp', 'temperature', 'conductivity', 'oxidation_reduction_potential']).values

    # Perform Incremental PCA
    ipca_env = IncrementalPCA(n_components=2)
    ipca_quality = IncrementalPCA(n_components=2)
    reduced_env = ipca_env.fit_transform(env_data)
    reduced_quality = ipca_quality.fit_transform(quality_data)

    # Perform CCA
    cca = CCA(n_components=2)
    cca.fit(reduced_env, reduced_quality)
    env_c, quality_c = cca.transform(reduced_env, reduced_quality)

    # Analyze canonical correlation
    canonical_corr = np.corrcoef(env_c.T, quality_c.T)[:2, 2:]
    print(f"Canonical Correlations:\n{canonical_corr}")

    # Optionally, detect anomalies
    if np.min(np.abs(canonical_corr)) < 0.5:
        send_alert("Anomaly detected in combined water and environmental data!")

def send_alert(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "water_quality_alerts",
        {
            "type": "send_water_quality_alert",
            "message": {"alert": message}
        }
    )
