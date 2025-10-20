from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.db import connection

class DashboardView(TemplateView):
    template_name = 'sales/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if sales tables exist
        tables_exist = self.check_sales_tables_exist()
        
        if tables_exist:
            try:
                from .models import Sale, Purchase, Customer, Product
                # Sales metrics
                context['sales_metrics'] = Sale.get_sales_metrics()
                context['purchase_metrics'] = Purchase.get_purchase_metrics()
                
                # Recent records
                context['recent_sales'] = Sale.objects.select_related('customer').prefetch_related('items__product').order_by('-sale_date')[:10]
                context['recent_purchases'] = Purchase.objects.select_related('customer').prefetch_related('items__product_category').order_by('-purchase_date')[:10]
                
                # Customer stats
                context['total_customers'] = Customer.objects.count()
                context['total_products'] = Product.objects.filter(is_active=True).count()
                context['tables_exist'] = True
                
            except Exception as e:
                context['tables_exist'] = False
                context['error'] = str(e)
        else:
            context['tables_exist'] = False
            context['setup_required'] = True
        
        return context

    def check_sales_tables_exist(self):
        """Check if sales tables exist in database"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sales_sale')")
                return cursor.fetchone()[0]
        except:
            return False

# ... keep the rest of your export functions ...
