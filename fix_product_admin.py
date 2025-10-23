# Fix Product admin to use actual fields
with open('sales/admin.py', 'r') as f:
    content = f.read()

# Replace the price field with actual fields
content = content.replace("list_display = ['name', 'price']", "list_display = ['name', 'category', 'created_at']")

with open('sales/admin.py', 'w') as f:
    f.write(content)

print(' Fixed Product admin to use actual fields')
