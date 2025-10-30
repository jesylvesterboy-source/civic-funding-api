from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import fss_tracker_dashboard, system_health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # ADD THIS LINE
    path('', root_view, name='home'),
    path('fsss-dashboard/', fss_tracker_dashboard, name='fsss_dashboard_alt'),
    path('fsss-dashboard/', fss_tracker_dashboard, name='fsss_dashboard_alt'),
    path('health-check/', system_health_check, name='system_health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Include this in your main urls.py
from django.urls import include, path

urlpatterns = [
    # ... existing patterns ...
    
    # Staff Performance
    path('staff-performance/', include('staff_performance.urls')),
    
    # Farmer Engagement
    path('farmer-engagement/', include('farmer_engagement.urls')),
    
    # Video Calls
    path('video-calls/', include('video_calls.urls')),
]
# Add to gates_tracker/urls.py
from django.http import JsonResponse
from django.urls import path

def health_check(request):
    return JsonResponse({"status": "healthy", "service": "FSSS Platform"})

urlpatterns = [
    path('health/', health_check, name='health_check'),
    # ... your existing URLs
]
