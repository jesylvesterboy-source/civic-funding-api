from django.contrib import admin
from .models import Location, Household, Farmer, FarmPlot

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'region', 'country']
    list_filter = ['district', 'region', 'country']
    search_fields = ['name', 'district']

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ['head_of_household', 'location', 'family_size', 'income_level']
    list_filter = ['income_level', 'location']
    search_fields = ['head_of_household']

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'household', 'phone_number']
    list_filter = ['gender', 'household__location']
    search_fields = ['first_name', 'last_name', 'phone_number']

@admin.register(FarmPlot)
class FarmPlotAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'location', 'size_acres', 'soil_type']
    list_filter = ['location', 'soil_type']
    search_fields = ['farmer__first_name', 'farmer__last_name']