# gates_tracker/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.apps import apps
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

@login_required
def fss_tracker_dashboard(request):
    """FSSS TRACKER SYSTEM - ROBUST DASHBOARD VIEW"""
    context = {
        'total_customers': 0,
        'total_projects': 0,
        'total_transactions': 0,
        'total_farmers': 0,
        'sales_metrics': {'total_revenue': 0, 'total_sales': 0, 'average_sale': 0},
        'all_models': [],
        'tables_exist': False,
        'system_status': 'initializing',
        'active_apps': []
    }
    
    try:
        # DATABASE-AGNOSTIC TABLE CHECK
        try:
            with connection.cursor() as cursor:
                # Try PostgreSQL syntax first
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                tables = [table[0] for table in cursor.fetchall()]
        except:
            try:
                # Fallback to SQLite syntax
                with connection.cursor() as cursor:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = [table[0] for table in cursor.fetchall()]
            except:
                tables = []
        
        context['tables_exist'] = len(tables) > 5  # Reasonable minimum
        context['system_status'] = 'operational' if context['tables_exist'] else 'initializing'
            
        # GET ALL MODELS WITH ROBUST ERROR HANDLING
        model_data = []
        
        for app_config in apps.get_app_configs():
            try:
                for model in app_config.get_models():
                    try:
                        count = model.objects.count()
                        admin_url = f'/admin/{app_config.label}/{model._meta.model_name}/'
                        
                        model_data.append({
                            'name': model._meta.verbose_name_plural.title(),
                            'app': app_config.verbose_name,
                            'app_label': app_config.label,
                            'model_name': model._meta.model_name,
                            'count': count,
                            'admin_url': admin_url
                        })
                    except Exception as model_error:
                        logger.debug(f'Could not count model {model._meta.model_name}: {model_error}')
                        continue
            except Exception as app_error:
                logger.warning(f'Error processing app {app_config.name}: {app_error}')
                continue
        
        context['all_models'] = model_data
        
        # GET SPECIFIC METRICS WITH FALLBACKS
        try:
            # Sales metrics
            if apps.is_installed('sales'):
                from sales.models import Customer, Sale
                context['total_customers'] = Customer.objects.count()
                sales = Sale.objects.all()
                context['sales_metrics']['total_sales'] = sales.count()
                total_revenue = sum(sale.total_amount for sale in sales if sale.total_amount)
                context['sales_metrics']['total_revenue'] = total_revenue or 0
                if context['sales_metrics']['total_sales'] > 0:
                    context['sales_metrics']['average_sale'] = context['sales_metrics']['total_revenue'] / context['sales_metrics']['total_sales']
        except Exception as sales_error:
            logger.warning(f'Sales metrics error: {sales_error}')
        
        try:
            # Project metrics
            if apps.is_installed('projects'):
                from projects.models import Project
                context['total_projects'] = Project.objects.count()
        except Exception as project_error:
            logger.warning(f'Project metrics error: {project_error}')
        
        try:
            # Financial metrics
            if apps.is_installed('finances'):
                from finances.models import Transaction
                context['total_transactions'] = Transaction.objects.count()
        except Exception as finance_error:
            logger.warning(f'Finance metrics error: {finance_error}')
        
        try:
            # Farmer metrics
            if apps.is_installed('farmers'):
                from farmers.models import Farmer
                context['total_farmers'] = Farmer.objects.count()
        except Exception as farmer_error:
            logger.warning(f'Farmer metrics error: {farmer_error}')
            
        # LOG SUCCESS
        logger.info(
            f"FSSS Dashboard loaded: {context['total_customers']} customers, "
            f"{context['total_projects']} projects, "
            f"{context['total_transactions']} transactions"
        )
        
    except Exception as major_error:
        logger.error(f'Major error in FSSS dashboard: {major_error}')
        context['system_status'] = 'error'
        messages.error(request, 'System temporarily unavailable')
    
    return render(request, 'fsss_dashboard.html', context)

def system_health_check(request):
    """Comprehensive system health check"""
    health_data = {
        'status': 'healthy',
        'database': 'connected',
        'tables': [],
        'apps': [],
        'issues': []
    }
    
    try:
        # Database-agnostic table check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                health_data['tables'] = [table[0] for table in cursor.fetchall()]
        except:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    health_data['tables'] = [table[0] for table in cursor.fetchall()]
            except Exception as e:
                health_data['database'] = 'error'
                health_data['issues'].append(f'Database error: {e}')
        
        # Check installed apps
        health_data['apps'] = [app.name for app in apps.get_app_configs()]
        
        # Basic checks
        if len(health_data['tables']) < 5:
            health_data['issues'].append('Few database tables detected')
            
        if not health_data['apps']:
            health_data['issues'].append('No apps configured')
            
        if health_data['issues']:
            health_data['status'] = 'degraded'
            
    except Exception as e:
        health_data['status'] = 'unhealthy'
        health_data['database'] = 'disconnected'
        health_data['issues'].append(f'System error: {e}')
    
    return render(request, 'health_check.html', health_data)
