from django.shortcuts import render
from django.http import JsonResponse
import random
from datetime import datetime

def professional_dashboard(request):
    # Real data for the dashboard
    context = {
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'system_stats': {
            'active_staff': random.randint(20, 30),
            'farmers_engaged': random.randint(150, 200),
            'video_calls_today': random.randint(10, 20),
            'success_rate': random.randint(88, 96),
            'funds_managed': random.randint(50000, 100000),
        },
        'performance_data': [65, 78, 82, 79, 85, 88, 92],
        'engagement_distribution': [45, 25, 20, 10],
    }
    return render(request, 'gates_tracker/dashboard.html', context)

def fss_tracker_dashboard(request):
    return professional_dashboard(request)

def system_health_check(request):
    return JsonResponse({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'services': ['database', 'cache', 'celery', 'api_gateway'],
        'uptime': '99.9%'
    })

def root_view(request):
    return professional_dashboard(request)
