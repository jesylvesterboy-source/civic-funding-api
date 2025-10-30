from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import fss_tracker_dashboard, system_health_check, root_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Enterprise Modules
    path('staff-performance/', include('staff_performance.urls')),
    path('farmer-engagement/', include('farmer_engagement.urls')),
    path('video-calls/', include('video_calls.urls')),
    
    # Core Application URLs
    path('', root_view, name='home'),
    path('fsss-dashboard/', fss_tracker_dashboard, name='fsss_dashboard'),
    path('health-check/', system_health_check, name='system_health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
