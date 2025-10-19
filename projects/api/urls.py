from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Public export endpoints (no authentication required)
    path('projects/export/csv/', views.public_export_csv, name='public-export-csv'),
    path('projects/export/excel/', views.public_export_excel, name='public-export-excel'),
]
