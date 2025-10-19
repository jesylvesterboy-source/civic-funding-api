from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/core/', include('core.api.urls')),
    path('api/projects/', include('projects.api.urls')),
    path('api/finances/', include('finances.api.urls')),
    path('api/farmers/', include('farmers.api.urls')),
    path('api/indicators/', include('indicators.api.urls')),
    path('api/reports/', include('reports.api.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
