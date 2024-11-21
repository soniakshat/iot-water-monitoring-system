from django.urls import path
from . import views
from . import consumers

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),       # Redirect root to the dashboard
    path('chart-data/', views.get_chart_data, name='chart_data'),  
]

websocket_urlpatterns = [
    path('ws/water-quality/', consumers.WaterQualityConsumer.as_asgi()),
]
