from django.contrib import admin
from .models import Farmer, FarmPlot

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'gender', 'date_of_birth', 
        'phone_number', 'education_level', 'household'
    ]
    list_filter = ['gender', 'education_level']
    search_fields = ['first_name', 'last_name', 'phone_number']

@admin.register(FarmPlot)
class FarmPlotAdmin(admin.ModelAdmin):
    list_display = [
        'farmer', 'size_acres', 'soil_type', 'gps_coordinates'
    ]
    list_filter = ['soil_type']
    search_fields = ['farmer__first_name', 'farmer__last_name', 'gps_coordinates']
