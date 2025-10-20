from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard_home'),
    path('export/<str:model_name>/', views.export_data, name='export_data'),
    path('api/live-metrics/', views.live_metrics_api, name='live_metrics'),
    path('api/impact-report/', views.impact_report, name='impact_report'),
]
