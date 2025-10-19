from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from farmers.models import Farmer, Household, Location
from .serializers import FarmerSerializer, HouseholdSerializer, LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return Location.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return Location.export_to_excel()

class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return Household.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return Household.export_to_excel()

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return Farmer.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return Farmer.export_to_excel()
