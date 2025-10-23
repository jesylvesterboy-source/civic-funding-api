# Enable delete in sales admin
with open('sales/admin.py', 'w') as f:
    f.write('''
from django.contrib import admin
from .models import Sale, Product, Purchase, Customer, Category

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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
''')

print(' Enabled delete in sales admin')
