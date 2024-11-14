import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA
from .models import WaterQualityData

def get_water_quality_data():
    data = WaterQualityData.objects.values(
        'pH', 'turbidity', 'dissolved_oxygen', 'conductivity', 'temperature',
        'nitrate', 'phosphate', 'total_organic_carbon', 'chlorine', 'ammonium',
        'heavy_metals', 'fluoride', 'oxidation_reduction_potential', 'biological_oxygen_demand'
    )
    return pd.DataFrame(list(data))

def perform_pca(df):
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df.fillna(0))
    return principal_components

def perform_cca(df):
    cca = CCA(n_components=2)
    df1 = df.iloc[:, :len(df.columns)//2]
    df2 = df.iloc[:, len(df.columns)//2:]
    cca.fit(df1, df2)
    X_c, Y_c = cca.transform(df1, df2)
    return X_c, Y_c
