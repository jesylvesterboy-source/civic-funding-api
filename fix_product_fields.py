# Fix Product admin to use actual fields
with open('sales/admin.py', 'r') as f:
    content = f.read()

# Replace with actual Product fields
content = content.replace(
    "list_display = ['name', 'category', 'created_at']", 
    "list_display = ['name', 'product_category', 'selling_price', 'current_stock']"
)

with open('sales/admin.py', 'w') as f:
    f.write(content)

print(' Fixed Product admin to use actual fields: name, product_category, selling_price, current_stock')
