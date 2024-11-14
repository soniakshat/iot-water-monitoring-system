from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),       # Redirect root to the dashboard
    path('pca/', views.pca_view, name='pca_analysis'),       # PCA analysis view
    path('cca/', views.cca_view, name='cca_analysis'),       # CCA analysis view
    path('chart-data/', views.get_chart_data, name='chart_data'),  
]
