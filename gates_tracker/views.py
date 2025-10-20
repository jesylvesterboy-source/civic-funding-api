from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

# Import our BEAUTIFUL new dashboard
from dashboard.views import home as dashboard_home

def fss_tracker_dashboard(request):
    """REDIRECT to our GORGEOUS new dashboard"""
    return dashboard_home(request)

def system_health_check(request):
    """System health check endpoint"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return HttpResponse("OK", status=200)
    except Exception as e:
        return HttpResponse(f"Database error: {e}", status=500)
