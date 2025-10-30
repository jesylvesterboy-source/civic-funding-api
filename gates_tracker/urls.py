from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    professional_dashboard, system_health_check, root_view,
    staff_performance_dashboard, farmer_engagement_dashboard, video_calls_dashboard,
    deployment_health_check  # Add this import
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/', include('sales.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # Enterprise Modules - Direct Dashboard Links
    path('staff-performance/', staff_performance_dashboard, name='staff_performance'),
    path('farmer-engagement/', farmer_engagement_dashboard, name='farmer_engagement'),
    path('video-calls/', video_calls_dashboard, name='video_calls'),

    # Core Application URLs
    path('', root_view, name='home'),
    path('dashboard/', professional_dashboard, name='dashboard'),
    path('health-check/', system_health_check, name='system_health_check'),
    path('deployment-health/', deployment_health_check, name='deployment_health'),  # Add this
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
