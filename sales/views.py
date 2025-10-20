from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Sale, Purchase, Customer, Product

class DashboardView(TemplateView):
    template_name = 'sales/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sales metrics
        context['sales_metrics'] = Sale.get_sales_metrics()
        context['purchase_metrics'] = Purchase.get_purchase_metrics()
        
        # Recent records with detailed item data
        recent_sales = Sale.objects.select_related('customer').prefetch_related('items__product').order_by('-sale_date')[:10]
        recent_purchases = Purchase.objects.select_related('customer').prefetch_related('items__product_category').order_by('-purchase_date')[:10]
        
        context['recent_sales'] = recent_sales
        context['recent_purchases'] = recent_purchases
        
        # Customer stats
        context['total_customers'] = Customer.objects.count()
        context['total_products'] = Product.objects.filter(is_active=True).count()
        
        return context

def export_sales_csv(request):
    return Sale.export_to_csv()

def export_purchases_csv(request):
    return Purchase.export_to_csv()

def export_customers_csv(request):
    return Customer.export_to_csv()

def export_sales_records_csv(request):
    """Export sales records with exact requested format"""
    return Sale.export_sales_records_csv()

def export_purchase_records_csv(request):
    """Export purchase records with exact requested format"""
    return Purchase.export_purchase_records_csv()
