from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard_home'),
    path('export/<str:model_name>/', views.export_data, name='export_data'),
    path('reports/', views.reports_main, name='reports_main'),
    path('reports/generate/<str:report_type>/', views.generate_report, name='generate_report'),
    path('api/live-metrics/', views.live_metrics_api, name='live_metrics'),
]
