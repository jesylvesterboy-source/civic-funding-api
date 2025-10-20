class DashboardView(TemplateView):
    template_name = 'sales/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sales metrics
        context['sales_metrics'] = Sale.get_sales_metrics()
        context['purchase_metrics'] = Purchase.get_purchase_metrics()
        
        # Recent records
        recent_sales = Sale.objects.select_related('customer').prefetch_related('items__product').order_by('-sale_date')[:10]
        recent_purchases = Purchase.objects.select_related('customer').prefetch_related('items__product_category').order_by('-purchase_date')[:10]
        
        context['recent_sales'] = recent_sales
        context['recent_purchases'] = recent_purchases
        
        # Customer stats
        context['total_customers'] = Customer.objects.count()
        context['total_products'] = Product.objects.filter(is_active=True).count()
        context['total_categories'] = ProductCategory.objects.count()
        
        # Chart Data
        context['chart_data'] = self.get_chart_data()
        
        return context

    def get_chart_data(self):
        """Generate data for all charts"""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count, Sum
        
        # Last 7 days for trend analysis
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        
        # Sales by day
        sales_by_day = Sale.objects.filter(
            sale_date__gte=start_date, 
            status='paid'
        ).extra({
            'date': "date(sale_date)"
        }).values('date').annotate(
            total=Sum('final_amount'),
            count=Count('id')
        ).order_by('date')
        
        # Payment method distribution
        payment_methods = Sale.objects.filter(status='paid').values(
            'payment_method'
        ).annotate(
            total=Sum('final_amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Customer demographics
        customer_gender = Customer.objects.values('gender').annotate(
            count=Count('id')
        )
        
        customer_age = Customer.objects.values('age_range').annotate(
            count=Count('id')
        )
        
        # Product categories sales
        product_sales = SaleItem.objects.values(
            'product__product_category__name'
        ).annotate(
            total=Sum('line_total'),
            quantity=Sum('quantity')
        ).order_by('-total')[:8]
        
        return {
            'sales_trend': list(sales_by_day),
            'payment_methods': list(payment_methods),
            'customer_gender': list(customer_gender),
            'customer_age': list(customer_age),
            'product_sales': list(product_sales),
            'dates': [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(8)]
        }
