from rest_framework import viewsets, permissions
from farmers.models import Farmer, Household, Location
from .serializers import FarmerSerializer, HouseholdSerializer, LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    permission_classes = [permissions.IsAuthenticated]

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]