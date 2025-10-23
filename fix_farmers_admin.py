# Enable delete in farmers admin
with open('farmers/admin.py', 'w') as f:
    f.write('''
from django.contrib import admin
from .models import Farmer, Household

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number']
    search_fields = ['first_name', 'last_name']
    actions = ['delete_selected']

@admin.register(Household)  
class HouseholdAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
''')

print(' Enabled delete in farmers admin')
