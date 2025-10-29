# staff_performance/urls.py
from django.urls import path
from . import views

app_name = 'staff_performance'

urlpatterns = [
    # Dashboard - WORKING
    path('', views.StaffPerformanceDashboard.as_view(), name='dashboard'),
    
    # Staff Management - WORKING
    path('staff/', views.StaffList.as_view(), name='staff_list'),
    path('staff/<uuid:staff_id>/', views.StaffDetail.as_view(), name='staff_detail'),
    
    # Performance Metrics - WORKING
    path('metrics/', views.PerformanceMetricList.as_view(), name='metric_list'),
    path('metrics/export/', views.export_performance_metrics, name='export_metrics'),
    
    # Performance Reviews - WORKING
    path('reviews/', views.PerformanceReviewList.as_view(), name='review_list'),
    
    # KPIs - WORKING
    path('kpis/', views.KPIList.as_view(), name='kpi_list'),
    path('kpis/export/', views.export_kpis, name='export_kpis'),
    
    # Reports - WORKING
    path('reports/performance/', views.PerformanceReport.as_view(), name='performance_report'),
    path('reports/export/', views.export_performance_report, name='export_performance_report'),
]
