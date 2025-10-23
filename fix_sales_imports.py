# Fix sales admin imports - only import what actually exists
with open('sales/admin.py', 'w') as f:
    f.write('''
from django.contrib import admin
from .models import Sale, Product, Purchase, Customer

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['customer', 'total_amount', 'sale_date']
    actions = ['delete_selected']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    actions = ['delete_selected']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

# Only register models that actually exist
''')

print(' Fixed sales admin imports')
