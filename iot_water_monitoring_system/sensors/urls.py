from django.urls import path
from . import views
from django.urls import re_path
from .consumers import NotificationConsumer

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('sse/notifications/', views.sse_notifications_stream, name='sse_notifications'),
    path('chart-data/', views.get_chart_data, name='chart_data'),
]

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
