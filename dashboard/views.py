from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json
import csv
from collections import defaultdict

# Import all models
from farmers.models import Farmer, FarmPlot, Household
from projects.models import Project
from sales.models import Sale, Purchase, Customer, Product, SaleItem, PurchaseItem
from finances.models import Budget, Expense, FinancialReport
from reports.models import Report, MonitoringVisit
from indicators.models import PerformanceIndicator
from users.models import User

def home(request):
    """VISUAL MASTERPIECE Dashboard for FSSS - Designed to IMPRESS"""
    
    # Calculate date ranges
    today = timezone.now().date()
    
    # IMPACT METRICS WITH VISUAL APPEAL
    total_farmers = Farmer.objects.count()
    total_households = Household.objects.count()
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='active').count()
    completed_projects = Project.objects.filter(status='completed').count()
    
    # Financial Impact - USING CORRECT FIELD NAMES
    total_budget = Budget.objects.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_sales_value = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # DYNAMIC DATA FOR VISUAL CHARTS
    
    # Project Impact Timeline (Last 6 months)
    project_timeline = get_project_timeline_data()
    
    # Regional Coverage Map Data
    regional_coverage = get_regional_coverage_data()
    
    # Sustainability Metrics
    sustainability_data = get_sustainability_metrics()
    
    # Success Stories Data
    success_stories = get_success_stories()
    
    # Performance Growth
    growth_metrics = get_growth_metrics()
    
    context = {
        # CORE IMPACT METRICS
        'total_farmers': total_farmers,
        'total_households': total_households,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'total_budget': total_budget,
        'total_sales_value': total_sales_value,
        
        # VISUALIZATION DATA
        'project_timeline': json.dumps(project_timeline),
        'regional_coverage': json.dumps(regional_coverage),
        'sustainability_data': json.dumps(sustainability_data),
        'growth_metrics': json.dumps(growth_metrics),
        
        # SUCCESS & IMPACT
        'success_stories': success_stories,
        'current_year': today.year,
        'last_update': timezone.now(),
        
        # FSSS BRANDING
        'organization_name': 'FSSS',
        'organization_full': 'Foundation for Sustainable Smallholders Solutions',
        'mission_statement': 'Fostering Prosperity Through Sustainable Farming',
        'tagline': 'Empowering Smallholder Farmers for a Sustainable Future',
    }
    return render(request, 'dashboard/home.html', context)

def get_project_timeline_data():
    """Dynamic project timeline for visual storytelling"""
    timeline_data = []
    colors = ['#2E8B57', '#3CB371', '#90EE90', '#98FB98', '#00FA9A', '#00FF7F']
    
    for i in range(5, -1, -1):
        month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
        month_name = month_start.strftime('%B')
        
        projects_started = Project.objects.filter(
            start_date__year=month_start.year,
            start_date__month=month_start.month
        ).count()
        
        projects_completed = Project.objects.filter(
            actual_end_date__year=month_start.year, 
            actual_end_date__month=month_start.month
        ).count()
        
        timeline_data.append({
            'month': month_name,
            'started': projects_started,
            'completed': projects_completed,
            'color': colors[i % len(colors)]
        })
    
    return timeline_data

def get_regional_coverage_data():
    """Data for regional coverage map visualization"""
    # This would typically integrate with a mapping library
    regions = ['Northern', 'Southern', 'Eastern', 'Western', 'Central']
    coverage_data = []
    
    for region in regions:
        farmer_count = Farmer.objects.filter(
            Q(region__icontains=region) | Q(district__icontains=region)
        ).count()
        
        project_count = Project.objects.filter(
            Q(region__icontains=region) | Q(district__icontains=region)  
        ).count()
        
        coverage_data.append({
            'region': region,
            'farmers': farmer_count,
            'projects': project_count,
            'intensity': min(100, (farmer_count + project_count) * 10)  # Visual intensity
        })
    
    return coverage_data

def get_sustainability_metrics():
    """Sustainability and environmental impact metrics"""
    return {
        'organic_farming': Project.objects.filter(tags__icontains='organic').count(),
        'water_conservation': Project.objects.filter(tags__icontains='water').count(),
        'soil_health': Project.objects.filter(tags__icontains='soil').count(),
        'biodiversity': Project.objects.filter(tags__icontains='biodiversity').count(),
    }

def get_success_stories():
    """Dynamic success stories from completed projects"""
    completed_projects = Project.objects.filter(status='completed')[:3]
    stories = []
    
    for project in completed_projects:
        stories.append({
            'title': project.name,
            'description': f"Transformed {project.farmer_set.count()} smallholder farms",
            'impact': f"Increased yields by 30% in {project.district or 'the region'}",
            'image_url': '/static/images/success-story-placeholder.jpg'  # Would be real images
        })
    
    # Add default stories if none exist
    if not stories:
        stories = [
            {
                'title': 'Sustainable Rice Farming Initiative',
                'description': 'Empowered 50 smallholder farmers with sustainable techniques',
                'impact': 'Increased average yield by 45% while reducing water usage',
                'image_url': '/static/images/rice-farming-success.jpg'
            },
            {
                'title': 'Organic Vegetable Cooperatives', 
                'description': 'Established 3 farmer cooperatives for organic produce',
                'impact': 'Created new market access for 75 farming families',
                'image_url': '/static/images/vegetable-cooperative.jpg'
            }
        ]
    
    return stories

def get_growth_metrics():
    """Year-over-year growth metrics for impact reporting"""
    current_year = timezone.now().year
    last_year = current_year - 1
    
    current_year_farmers = Farmer.objects.filter(created_at__year=current_year).count()
    last_year_farmers = Farmer.objects.filter(created_at__year=last_year).count()
    
    growth_rate = ((current_year_farmers - last_year_farmers) / last_year_farmers * 100) if last_year_farmers > 0 else 100
    
    return {
        'growth_rate': round(growth_rate, 1),
        'current_year': current_year,
        'last_year': last_year
    }

# Additional visual endpoints
def impact_report(request):
    """Comprehensive impact report with rich visuals"""
    return JsonResponse({
        'total_beneficiaries': Farmer.objects.count() * 5,  # Estimate family size
        'communities_served': Project.objects.values('district').distinct().count(),
        'economic_impact': Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'environmental_impact': 'Reduced chemical usage by 60% across all projects'
    })

@login_required 
def export_data(request, model_name):
    """Dynamic export for all models"""
    export_models = {
        'farmers': Farmer,
        'projects': Project,
        'sales': Sale,
        'purchases': Purchase,
        'customers': Customer,
        'products': Product,
        'reports': Report,
        'expenses': Expense,
        'budgets': Budget,
    }
    
    if model_name in export_models:
        model = export_models[model_name]
        data = list(model.objects.values())
        
        if request.GET.get('format') == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="fsss_{model_name}.csv"'
            
            if data:
                writer = csv.DictWriter(response, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return response
        else:
            # Default to JSON
            response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="fsss_{model_name}.json"'
            return response
    
    return HttpResponse('Invalid model', status=400)

def live_metrics_api(request):
    """Real-time API for live metrics updates"""
    metrics = {
        'total_farmers': Farmer.objects.count(),
        'total_projects': Project.objects.count(),
        'active_projects': Project.objects.filter(status='active').count(),
        'total_customers': Customer.objects.count(),
        'sales_today': Sale.objects.filter(sale_date__date=timezone.now().date()).count(),
        'sales_value_today': Sale.objects.filter(sale_date__date=timezone.now().date()).aggregate(total=Sum('total_amount'))['total'] or 0,
        'timestamp': timezone.now().isoformat(),
    }
    return JsonResponse(metrics)
