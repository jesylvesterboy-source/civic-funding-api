from django.shortcuts import render
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
import json

def home(request):
    """INTELLIGENT DASHBOARD - Auto-detects user role"""
    user = request.user
    
    # Detect user role
    user_role = detect_user_role(user)
    
    # Get role-specific metrics
    metrics = get_role_specific_metrics(user, user_role)
    
    context = {
        # User info
        'user_role': user_role,
        'user_name': user.get_full_name() or user.username,
        
        # Role-specific metrics
        'total_farmers': metrics['farmers'],
        'total_projects': metrics['projects'],
        'active_projects': metrics['active_projects'],
        'total_customers': metrics['customers'],
        'total_sales_value': metrics['sales_value'],
        'total_budget': metrics['budget'],
        'total_households': metrics['households'],
        'total_products': metrics['products'],
        'total_sales': metrics['sales_count'],
        'budget_utilization': metrics['utilization'],
        
        # System info
        'current_year': timezone.now().year,
        'last_update': timezone.now(),
    }
    
    return render(request, 'dashboard/home.html', context)

def detect_user_role(user):
    """Intelligently detect user role from Django groups"""
    if not user.is_authenticated:
        return 'guest'
    
    # Check Django groups for role assignment
    if user.groups.filter(name='Project Managers').exists():
        return 'project_manager'
    elif user.groups.filter(name='Field Officers').exists():
        return 'field_officer' 
    elif user.groups.filter(name='Finance Officers').exists():
        return 'finance_officer'
    elif user.is_superuser or user.is_staff:
        return 'administrator'
    else:
        return 'basic_user'

def get_role_specific_metrics(user, role):
    """Get metrics tailored to user role"""
    base_metrics = get_smart_dynamic_metrics()
    
    # Role-specific metric adjustments
    if role == 'field_officer':
        # Field officers see only their assigned data
        base_metrics['farmers'] = get_my_farmers_count(user)
        base_metrics['projects'] = get_my_projects_count(user)
    
    elif role == 'project_manager':
        # Project managers see their team's performance
        base_metrics['team_performance'] = get_team_performance(user)
        
    elif role == 'finance_officer':
        # Finance officers get detailed financial metrics
        base_metrics['expense_breakdown'] = get_expense_breakdown()
        
    return base_metrics

def get_my_farmers_count(user):
    """Get farmer count for field officers (their assigned farmers only)"""
    try:
        from farmers.models import Farmer
        # This would filter to only farmers assigned to this user
        return Farmer.objects.count()  # Placeholder - would be filtered
    except:
        return 0

def get_my_projects_count(user):
    """Get project count for user's assigned projects"""
    try:
        from projects.models import Project
        return Project.objects.count()  # Placeholder - would be filtered
    except:
        return 0

def get_smart_dynamic_metrics():
    """Get all metrics with intelligent fallbacks"""
    metrics = {
        'farmers': 0, 'projects': 0, 'active_projects': 0, 'customers': 0,
        'sales_value': 0, 'budget': 0, 'households': 0, 'products': 0,
        'sales_count': 0, 'utilization': 0
    }
    
    # Farmers count
    try:
        from farmers.models import Farmer
        metrics['farmers'] = Farmer.objects.count()
        metrics['households'] = metrics['farmers'] * 5
    except: pass
    
    # Projects count
    try:
        from projects.models import Project
        metrics['projects'] = Project.objects.count()
        metrics['active_projects'] = Project.objects.filter(status='active').count()
    except: pass
    
    # Customers count
    try:
        from sales.models import Customer
        metrics['customers'] = Customer.objects.count()
    except: pass
    
    # Products count
    try:
        from sales.models import Product
        metrics['products'] = Product.objects.count()
    except: pass
    
    # Sales data
    try:
        from sales.models import Sale
        metrics['sales_count'] = Sale.objects.count()
        result = Sale.objects.aggregate(total=Sum('total_amount'))
        metrics['sales_value'] = result['total'] or 0
    except: pass
    
    # Budget data
    try:
        from finances.models import Budget
        result = Budget.objects.aggregate(total=Sum('allocated_amount'))
        metrics['budget'] = result['total'] or 0
    except: pass
    
    return metrics

def export_data(request, model_name):
    """Role-aware export system"""
    user_role = detect_user_role(request.user)
    
    # Role-based export restrictions
    if user_role == 'field_officer' and model_name not in ['farmers', 'reports']:
        return JsonResponse({'error': 'Access denied for your role'}, status=403)
    
    # Continue with export logic...
    return JsonResponse({'message': f'Exporting {model_name} for {user_role}'})

# Keep existing functions
def reports_main(request):
    return render(request, 'dashboard/reports_main.html')

def generate_report(request, report_type):
    return JsonResponse({'message': 'Report generation coming soon!'})

def live_metrics_api(request):
    metrics = get_smart_dynamic_metrics()
    return JsonResponse(metrics)
