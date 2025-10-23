# Add the missing models that actually exist
with open('sales/admin.py', 'a') as f:
    f.write('''
from .models import ProductCategory, SaleItem, PurchaseItem

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
''')

print(' Added missing models to sales admin')
