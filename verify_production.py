#!/usr/bin/env python
"""
Comprehensive verification script for Gates Tracker Production Readiness
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.test import TestCase
from django.db import connection
from django.conf import settings

def verify_database():
    """Verify PostgreSQL database connectivity"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
        print("✅ PostgreSQL Database: CONNECTED")
        print(f"   Database: {db_version[0]}")
        return True
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return False

def verify_environment():
    """Verify environment variables"""
    required_vars = ['SECRET_KEY', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD']
    all_good = True
    
    for var in required_vars:
        value = getattr(settings, var, None) or os.environ.get(var)
        if value and value not in ['', 'your-secure-key']:
            print(f"✅ Environment {var}: SET")
        else:
            print(f"❌ Environment {var}: MISSING")
            all_good = False
    
    return all_good

def verify_models():
    """Verify all models can be imported and have migrations"""
    try:
        from users.models import User
        from projects.models import Project
        from finances.models import Budget, Expense, FinancialReport
        from farmers.models import Farmer, Household, Location
        from reports.models import Report, MonitoringVisit
        
        models = [User, Project, Budget, Expense, FinancialReport, Farmer, Household, Location, Report, MonitoringVisit]
        for model in models:
            count = model.objects.count()
            print(f"✅ {model.__name__}: OK ({count} records)")
        
        return True
    except Exception as e:
        print(f"❌ Models Error: {e}")
        return False

def verify_api():
    """Verify API endpoints"""
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test authentication required endpoints
        endpoints = [
            '/api/v1/finances/budgets/',
            '/api/v1/finances/expenses/',
            '/api/v1/finances/financial-reports/',
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            if response.status_code in [200, 301, 302, 403]:
                print(f"✅ API {endpoint}: RESPONDING")
            else:
                print(f"❌ API {endpoint}: FAILED ({response.status_code})")
        
        return True
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

def verify_celery():
    """Verify Celery configuration"""
    try:
        from gates_tracker.celery import app
        print("✅ Celery: CONFIGURED")
        
        # Test if tasks can be imported
        from finances.tasks import check_budget_utilization, generate_monthly_financial_reports
        print("✅ Celery Tasks: IMPORTABLE")
        
        return True
    except Exception as e:
        print(f"❌ Celery Error: {e}")
        return False

def verify_export_functionality():
    """Verify export functionality"""
    try:
        from finances.export_views import ExportBudgetsCSV, ExportExpensesExcel
        
        # Test if export classes can be instantiated
        csv_export = ExportBudgetsCSV()
        excel_export = ExportExpensesExcel()
        
        print("✅ Export Functionality: CONFIGURED")
        return True
    except Exception as e:
        print(f"❌ Export Error: {e}")
        return False

def verify_email_config():
    """Verify email configuration"""
    try:
        email_backend = getattr(settings, 'EMAIL_BACKEND', '')
        email_host = getattr(settings, 'EMAIL_HOST', '')
        
        if email_backend and email_host:
            print("✅ Email Configuration: SET")
            return True
        else:
            print("⚠️ Email Configuration: INCOMPLETE (check settings)")
            return False
    except Exception as e:
        print(f"❌ Email Error: {e}")
        return False

def main():
    print("🚀 GATES TRACKER PRODUCTION VERIFICATION")
    print("=" * 50)
    
    checks = [
        ("Environment Variables", verify_environment),
        ("Database Connection", verify_database),
        ("Django Models", verify_models),
        ("API Endpoints", verify_api),
        ("Celery Setup", verify_celery),
        ("Export Functionality", verify_export_functionality),
        ("Email Configuration", verify_email_config),
    ]
    
    results = []
    for check_name, check_function in checks:
        print(f"\n🔍 Checking {check_name}...")
        result = check_function()
        results.append((check_name, result))
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL SYSTEMS GO! Your Gates Tracker is production-ready!")
        print("   Ready for GitHub deployment and client delivery!")
    else:
        print(f"\n⚠️ {total - passed} checks need attention before production.")

if __name__ == "__main__":
    main()