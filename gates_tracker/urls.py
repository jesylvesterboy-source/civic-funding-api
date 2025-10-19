from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render

def home_dashboard(request):
    return render(request, 'home_dashboard.html')

def public_home(request):
    return render(request, 'public_home.html')

urlpatterns = [
    path('', public_home, name='home'),
    path('dashboard/', home_dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    
    # API endpoints
    path('api/projects/', include('projects.api.urls')),
    path('api/farmers/', include('farmers.api.urls')),
    path('api/finances/', include('finances.api.urls')),
    path('api/indicators/', include('indicators.api.urls')),
    path('api/reports/', include('reports.api.urls')),
    path('api/core/', include('core.api.urls')),  # Dashboard metrics APIs
]
