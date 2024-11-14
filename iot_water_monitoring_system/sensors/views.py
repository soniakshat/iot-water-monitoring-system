from django.shortcuts import render
from .analysis import get_water_quality_data, perform_pca, perform_cca
import plotly.express as px
from .models import WaterQualityData
import pandas as pd
from datetime import timedelta

def dashboard_view(request):
    # Retrieve all data from WaterQualityData model
    data = WaterQualityData.objects.all().values('timestamp', 'pH', 'turbidity', 'dissolved_oxygen', 'conductivity', 'temperature', 'nitrate', 'phosphate', 'total_organic_carbon', 'chlorine', 'ammonium', 'heavy_metals', 'fluoride', 'oxidation_reduction_potential', 'biological_oxygen_demand')
    df = pd.DataFrame(data)
    
    # Ensure the data is sorted by timestamp
    df = df.sort_values('timestamp')
    
    # Generate a time series chart for each parameter
    charts = {}
    parameters = ['pH', 'turbidity', 'dissolved_oxygen', 'conductivity', 'temperature', 'nitrate', 'phosphate', 'total_organic_carbon', 'chlorine', 'ammonium', 'heavy_metals', 'fluoride', 'oxidation_reduction_potential', 'biological_oxygen_demand']
    
    for param in parameters:
        fig = px.line(df, x='timestamp', y=param, title=f'{param} over Time')
        charts[param] = fig.to_html(full_html=False)  # Convert Plotly figure to HTML

    return render(request, 'sensors/dashboard.html', {'charts': charts})

def pca_view(request):
    df = get_water_quality_data()
    pca_results = perform_pca(df)
    fig = px.scatter(x=pca_results[:, 0], y=pca_results[:, 1], title="PCA Analysis of Water Quality Data")
    graph_div = fig.to_html(full_html=False)
    return render(request, 'sensors/analysis.html', {'graph': graph_div, 'title': 'PCA Analysis'})

def cca_view(request):
    df = get_water_quality_data()
    cca_x, cca_y = perform_cca(df)
    fig = px.scatter(x=cca_x[:, 0], y=cca_y[:, 0], title="CCA Analysis of Water Quality Data")
    graph_div = fig.to_html(full_html=False)
    return render(request, 'sensors/analysis.html', {'graph': graph_div, 'title': 'CCA Analysis'})
