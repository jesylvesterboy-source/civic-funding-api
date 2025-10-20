from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from sales.models import Sale, Purchase, Customer, Product

class RootDashboardView(TemplateView):
    template_name = 'root_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get metrics from all apps
        context['sales_metrics'] = Sale.get_sales_metrics() if hasattr(Sale, 'get_sales_metrics') else {}
        context['purchase_metrics'] = Purchase.get_purchase_metrics() if hasattr(Purchase, 'get_purchase_metrics') else {}
        
        # System overview
        context['total_customers'] = Customer.objects.count()
        context['total_products'] = Product.objects.filter(is_active=True).count() if hasattr(Product, 'objects') else 0
        context['total_sales'] = Sale.objects.count() if hasattr(Sale, 'objects') else 0
        context['total_purchases'] = Purchase.objects.count() if hasattr(Purchase, 'objects') else 0
        
        # Recent activity
        context['recent_sales'] = Sale.objects.select_related('customer').order_by('-sale_date')[:5] if hasattr(Sale, 'objects') else []
        context['recent_purchases'] = Purchase.objects.select_related('customer').order_by('-purchase_date')[:5] if hasattr(Purchase, 'objects') else []
        
        return context
