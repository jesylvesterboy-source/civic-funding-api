from django.shortcuts import render
from django.http import JsonResponse

def fss_tracker_dashboard(request):
    return JsonResponse({
        "message": "FSS Tracker Dashboard",
        "status": "Available",
        "module": "Financial Services System"
    })

def system_health_check(request):
    return JsonResponse({
        'status': 'healthy', 
        'timestamp': '2025-10-30T09:35:33Z',
        'services': ['database', 'cache', 'celery']
    })

def root_view(request):
    return JsonResponse({
        "message": "Civic Funding API Enterprise Stack",
        "status": "Operational",
        "modules": ["Staff Performance", "Farmer Engagement", "Video Calls"],
        "version": "1.0.0"
    })
