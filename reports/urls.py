from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_main, name='reports_main'),
    path('dashboard/', views.reports_dashboard, name='reports_dashboard'),
    path('financial/', views.financial_reports, name='financial_reports'),
    path('projects/', views.project_reports, name='project_reports'),
]
