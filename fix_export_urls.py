# Read the template
with open('dashboard/templates/dashboard/home.html', 'r') as f:
    content = f.read()

# Fix the export URLs
content = content.replace('/dashboard/export/farmers/', '/export/farmers/')
content = content.replace('/dashboard/export/projects/', '/export/projects/') 
content = content.replace('/dashboard/export/sales/', '/export/sales/')

# Write back
with open('dashboard/templates/dashboard/home.html', 'w') as f:
    f.write(content)

print(' Fixed export URLs in dashboard template')
print(' Export links will now work correctly')
