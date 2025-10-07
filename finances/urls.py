from django.urls import path
from . import views, export_views

urlpatterns = [
    # Financial dashboard and summaries
    path('dashboard/', views.financial_dashboard, name='financial-dashboard'),
    path('projects/<int:project_id>/financial-summary/', views.project_financial_summary, name='project-financial-summary'),

    # Export-related URLs
    path('export/budgets/csv/', export_views.ExportBudgetsCSV.as_view(), name='export-budgets-csv'),
    path('export/expenses/excel/', export_views.ExportExpensesExcel.as_view(), name='export-expenses-excel'),
    path('export/financial-reports/<int:report_id>/pdf/', export_views.ExportFinancialReportPDF.as_view(), name='export-financial-report-pdf'),
]