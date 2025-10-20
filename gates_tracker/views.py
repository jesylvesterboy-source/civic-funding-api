from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db import connection

class RootDashboardView(TemplateView):
    template_name = 'root_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if tables exist
        tables_exist = self.check_tables_exist()
        
        if tables_exist:
            try:
                from sales.models import Sale, Purchase, Customer, Product
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
                context['tables_exist'] = True
                
            except Exception as e:
                context['tables_exist'] = False
                context['error'] = str(e)
        else:
            context['tables_exist'] = False
            context['setup_required'] = True
        
        return context

    def check_tables_exist(self):
        """Check if sales tables exist in database"""
        try:
            from sales.models import Sale
            # Try a simple query to check if table exists
            Sale.objects.exists()
            return True
        except:
            return False
