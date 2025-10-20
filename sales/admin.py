from django.contrib import admin
from .models import (
    Customer, ProductCategory, Product, 
    Sale, SaleItem, Purchase, PurchaseItem
)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ['product', 'quantity', 'unit_price', 'line_total']
    readonly_fields = ['line_total']

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    fields = ['product_category', 'product_name', 'product_attribute', 'unit_measure', 'quantity', 'unit_price', 'line_total']
    readonly_fields = ['line_total']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'gender', 'age_range', 'loyalty_tier', 'total_purchases', 'purchase_count']
    list_filter = ['gender', 'age_range', 'loyalty_tier', 'customer_since']
    search_fields = ['name', 'phone_number', 'email']
    readonly_fields = ['customer_since', 'total_purchases', 'average_order_value']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_category', 'current_stock', 'selling_price', 'profit_margin', 'needs_restock']
    list_filter = ['product_category', 'is_active']
    search_fields = ['name', 'brand', 'variety', 'sku']
    readonly_fields = ['profit_margin', 'needs_restock']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'customer', 'sale_date', 'final_amount', 'status', 'payment_method']
    list_filter = ['status', 'payment_method', 'sales_channel', 'sale_date']
    search_fields = ['sale_number', 'customer__name', 'customer__phone_number']
    readonly_fields = ['sale_number', 'sale_date', 'total_amount', 'final_amount']
    inlines = [SaleItemInline]

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_number', 'customer', 'purchase_date', 'total_amount', 'status', 'supplier']
    list_filter = ['status', 'purchase_date']
    search_fields = ['purchase_number', 'customer__name', 'supplier']
    readonly_fields = ['purchase_number', 'purchase_date', 'total_amount']
    inlines = [PurchaseItemInline]

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    search_fields = ['name']

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'product', 'quantity', 'unit_price', 'line_total', 'attribute_name']
    list_filter = ['sale__sale_date']

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'product_name', 'product_attribute', 'quantity', 'unit_price', 'line_total']
    list_filter = ['purchase__purchase_date']
