from rest_framework import serializers
from farmers.models import Farmer, Household, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class HouseholdSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = Household
        fields = '__all__'

class FarmerSerializer(serializers.ModelSerializer):
    household_name = serializers.CharField(source='household.head_of_household', read_only=True)
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Farmer
        fields = '__all__'