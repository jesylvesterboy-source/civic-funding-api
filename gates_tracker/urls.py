from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# API Versioning imports
from api.v1.urls import urlpatterns as api_v1_urls

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # User authentication
    path('users/', include('users.urls')),
    
    # API Version 1
    path('api/v1/', include(api_v1_urls)),
    
    # API Authentication
    path('api-auth/', include('rest_framework.urls')),
    
    # Redirect root to dashboard
    path('', RedirectView.as_view(url='/users/dashboard/', permanent=False)),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)