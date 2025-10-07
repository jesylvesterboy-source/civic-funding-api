from django.urls import path, include

urlpatterns = [
    path('finances/', include('api.v1.finances.urls')),
    path('projects/', include('projects.api.urls')),
    path('farmers/', include('farmers.api.urls')),
]