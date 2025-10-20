from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('export/sales/', views.export_sales_csv, name='export_sales'),
    path('export/purchases/', views.export_purchases_csv, name='export_purchases'),
    path('export/customers/', views.export_customers_csv, name='export_customers'),
    path('export/sales-records/', views.export_sales_records_csv, name='export_sales_records'),
    path('export/purchase-records/', views.export_purchase_records_csv, name='export_purchase_records'),
]
