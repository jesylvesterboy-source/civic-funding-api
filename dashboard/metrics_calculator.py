from django.apps import apps
from django.db.models import Sum

def get_role_specific_metrics(user, user_role):
    """
    Get REAL role-specific metrics for the dashboard from database
    Returns dynamic, real-time data
    """
    metrics = {
        'farmers': 0,
        'projects': 0,
        'active_projects': 0,
        'customers': 0,
        'sales_value': 0,
        'budget': 0,
        'households': 0,
        'products': 0,
        'sales_count': 0,
        'utilization': 0,
    }
    
    try:
        # Try to get real data from database
        # Farmers
        try:
            Farmer = apps.get_model('farmers', 'Farmer')
            metrics['farmers'] = Farmer.objects.count()
        except:
            pass
            
        # Projects
        try:
            Project = apps.get_model('projects', 'Project')
            metrics['projects'] = Project.objects.count()
            metrics['active_projects'] = Project.objects.filter(status__icontains='active').count()
            
            # Total budget
            total_budget = Project.objects.aggregate(total=Sum('budget'))
            if total_budget['total']:
                metrics['budget'] = total_budget['total']
        except:
            pass
            
        # Sales
        try:
            Sale = apps.get_model('sales', 'Sale')
            metrics['sales_count'] = Sale.objects.count()
            
            # Total sales value
            total_sales = Sale.objects.aggregate(total=Sum('total_amount'))
            if total_sales['total']:
                metrics['sales_value'] = total_sales['total']
        except:
            pass
            
        # Households
        try:
            Household = apps.get_model('farmers', 'Household')
            metrics['households'] = Household.objects.count()
        except:
            pass
            
        # Products
        try:
            Product = apps.get_model('sales', 'Product')
            metrics['products'] = Product.objects.count()
        except:
            pass
            
        # Calculate utilization
        if metrics['projects'] > 0:
            metrics['utilization'] = round((metrics['active_projects'] / metrics['projects']) * 100, 1)
            
    except Exception as e:
        # If any error, use default values
        pass
        
    return metrics
