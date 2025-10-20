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
    """FSSS TRACKER SYSTEM - ULTRA ROBUST DASHBOARD VIEW"""
    # ULTRA ROBUST CONTEXT - Works even if everything fails
    context = {
        'total_customers': 0,
        'total_projects': 0,
        'total_transactions': 0,
        'total_farmers': 0,
        'sales_metrics': {'total_revenue': 0, 'total_sales': 0, 'average_sale': 0},
        'all_models': [],
        'tables_exist': False,
        'system_status': 'initializing',
        'active_apps': [],
        'modules_available': {
            'sales': False,
            'projects': False, 
            'finances': False,
            'farmers': False
        }
    }
    
    try:
        # ULTRA ROBUST DATABASE CHECK - Works with any database
        tables = []
        try:
            with connection.cursor() as cursor:
                # Try multiple database systems
                try:
                    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                    tables = [table[0] for table in cursor.fetchall()]
                except:
                    try:
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        tables = [table[0] for table in cursor.fetchall()]
                    except:
                        # Try MySQL syntax as fallback
                        try:
                            cursor.execute("SHOW TABLES;")
                            tables = [table[0] for table in cursor.fetchall()]
                        except:
                            tables = []
        except Exception as db_error:
            logger.warning(f"Database check failed: {db_error}")
            tables = []
        
        context['tables_exist'] = len(tables) > 3
        context['system_status'] = 'operational' if context['tables_exist'] else 'initializing'
            
        # ULTRA ROBUST MODEL DISCOVERY - Never crashes
        model_data = []
        installed_apps = []
        
        for app_config in apps.get_app_configs():
            app_name = app_config.name
            installed_apps.append(app_name)
            
            try:
                for model in app_config.get_models():
                    try:
                        # ULTRA SAFE MODEL COUNTING
                        count = 0
                        try:
                            # Check if table exists before counting
                            table_name = model._meta.db_table
                            if any(table_name.lower() in table.lower() for table in tables):
                                count = model.objects.count()
                            else:
                                count = 0
                        except:
                            count = 0
                            
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
                        logger.debug(f'Model processing skipped: {model._meta.model_name} - {model_error}')
                        continue
            except Exception as app_error:
                logger.debug(f'App processing skipped: {app_name} - {app_error}')
                continue
        
        context['all_models'] = model_data
        context['active_apps'] = installed_apps
        
        # ULTRA ROBUST METRICS COLLECTION - Each module independent
        try:
            # Sales metrics - COMPLETELY ISOLATED
            if apps.is_installed('sales'):
                context['modules_available']['sales'] = True
                try:
                    from sales.models import Customer, Sale
                    # Check if sales tables exist
                    if any('sales_customer' in table.lower() for table in tables):
                        context['total_customers'] = Customer.objects.count()
                    if any('sales_sale' in table.lower() for table in tables):
                        sales = Sale.objects.all()
                        context['sales_metrics']['total_sales'] = sales.count()
                        try:
                            total_revenue = sum(sale.total_amount for sale in sales if hasattr(sale, 'total_amount') and sale.total_amount)
                            context['sales_metrics']['total_revenue'] = total_revenue or 0
                            if context['sales_metrics']['total_sales'] > 0:
                                context['sales_metrics']['average_sale'] = context['sales_metrics']['total_revenue'] / context['sales_metrics']['total_sales']
                        except:
                            context['sales_metrics']['total_revenue'] = 0
                except ImportError:
                    logger.debug("Sales models not available")
                except Exception as sales_error:
                    logger.debug(f"Sales metrics skipped: {sales_error}")
        except Exception as sales_module_error:
            logger.debug(f"Sales module check failed: {sales_module_error}")
        
        try:
            # Project metrics - COMPLETELY ISOLATED
            if apps.is_installed('projects'):
                context['modules_available']['projects'] = True
                try:
                    from projects.models import Project
                    if any('projects_project' in table.lower() for table in tables):
                        context['total_projects'] = Project.objects.count()
                except ImportError:
                    logger.debug("Projects models not available")
                except Exception as project_error:
                    logger.debug(f"Project metrics skipped: {project_error}")
        except Exception as project_module_error:
            logger.debug(f"Project module check failed: {project_module_error}")
        
        try:
            # Financial metrics - COMPLETELY ISOLATED with multiple fallbacks
            if apps.is_installed('finances'):
                context['modules_available']['finances'] = True
                try:
                    # Try multiple possible model names
                    transaction_count = 0
                    try:
                        from finances.models import Transaction
                        if any('transaction' in table.lower() for table in tables):
                            transaction_count = Transaction.objects.count()
                    except ImportError:
                        try:
                            from finances.models import transaction
                            if any('transaction' in table.lower() for table in tables):
                                transaction_count = transaction.objects.count()
                        except ImportError:
                            try:
                                from finances.models import FinancialTransaction
                                if any('transaction' in table.lower() for table in tables):
                                    transaction_count = FinancialTransaction.objects.count()
                            except ImportError:
                                pass
                    context['total_transactions'] = transaction_count
                except Exception as finance_error:
                    logger.debug(f"Finance metrics skipped: {finance_error}")
        except Exception as finance_module_error:
            logger.debug(f"Finance module check failed: {finance_module_error}")
        
        try:
            # Farmer metrics - COMPLETELY ISOLATED
            if apps.is_installed('farmers'):
                context['modules_available']['farmers'] = True
                try:
                    from farmers.models import Farmer
                    if any('farmers_farmer' in table.lower() for table in tables):
                        context['total_farmers'] = Farmer.objects.count()
                except ImportError:
                    logger.debug("Farmers models not available")
                except Exception as farmer_error:
                    logger.debug(f"Farmer metrics skipped: {farmer_error}")
        except Exception as farmer_module_error:
            logger.debug(f"Farmer module check failed: {farmer_module_error}")
            
        # SUCCESS LOGGING
        logger.info("FSSS Dashboard loaded successfully with robust error handling")
        
    except Exception as major_error:
        # ULTIMATE FALLBACK - System never crashes
        logger.error(f'CRITICAL ERROR in FSSS dashboard: {major_error}')
        context['system_status'] = 'degraded'
        messages.warning(request, 'System is initializing - some features may be limited')
    
    # ULTRA ROBUST TEMPLATE RENDERING
    try:
        return render(request, 'fsss_dashboard.html', context)
    except:
        # FALLBACK TO SIMPLE RESPONSE
        from django.http import HttpResponse
        return HttpResponse(f"""
        <html>
        <head><title>FSSS Tracker System</title></head>
        <body>
            <h1>FSSS Tracker System - Initializing</h1>
            <p>Foundation for Sustainable Smallholder Solutions</p>
            <p>System is being configured. Projects: {context['total_projects']}, Customers: {context['total_customers']}</p>
            <a href="/admin/">Admin Panel</a> | <a href="/accounts/login/">Login</a>
        </body>
        </html>
        """)

def system_health_check(request):
    """ULTRA ROBUST SYSTEM HEALTH CHECK"""
    health_data = {
        'status': 'healthy',
        'database': 'connected', 
        'tables': [],
        'apps': [],
        'modules': {},
        'issues': []
    }
    
    try:
        # ULTRA ROBUST DATABASE CHECK
        try:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                    health_data['tables'] = [table[0] for table in cursor.fetchall()]
                except:
                    try:
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        health_data['tables'] = [table[0] for table in cursor.fetchall()]
                    except:
                        health_data['database'] = 'error'
                        health_data['issues'].append('Database system detection failed')
        except Exception as e:
            health_data['database'] = 'disconnected'
            health_data['issues'].append(f'Database connection failed: {e}')
        
        # ULTRA ROBUST APP CHECK
        health_data['apps'] = [app.name for app in apps.get_app_configs()]
        
        # MODULE SPECIFIC CHECKS
        modules_to_check = ['sales', 'projects', 'finances', 'farmers']
        for module in modules_to_check:
            try:
                if apps.is_installed(module):
                    health_data['modules'][module] = 'installed'
                    # Check if module has tables
                    module_tables = [t for t in health_data['tables'] if module in t.lower()]
                    health_data['modules'][f'{module}_tables'] = len(module_tables)
                else:
                    health_data['modules'][module] = 'not_installed'
            except:
                health_data['modules'][module] = 'check_failed'
        
        # HEALTH ASSESSMENT
        if len(health_data['tables']) < 5:
            health_data['issues'].append('Limited database tables detected')
            
        if not health_data['apps']:
            health_data['issues'].append('No apps configured')
            
        if health_data['issues']:
            health_data['status'] = 'degraded'
            
    except Exception as e:
        health_data['status'] = 'unhealthy'
        health_data['issues'].append(f'Health check system error: {e}')
    
    return render(request, 'health_check.html', health_data)
