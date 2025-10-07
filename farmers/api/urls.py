from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'locations', views.LocationViewSet)
router.register(r'households', views.HouseholdViewSet)
router.register(r'farmers', views.FarmerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]