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
    path('', fss_tracker_dashboard, name='fsss_dashboard'),
    path('fsss-dashboard/', fss_tracker_dashboard, name='fsss_dashboard_alt'),
    path('health-check/', system_health_check, name='system_health_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
