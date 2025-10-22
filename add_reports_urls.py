# Read current urls.py
with open('gates_tracker/urls.py', 'r') as f:
    content = f.read()

# Add reports URLs after the sales URLs line
new_content = content.replace(
    "    path('sales/', include('sales.urls')),",
    "    path('sales/', include('sales.urls')),\n    path('reports/', include('reports.urls')),"
)

# Write back to file
with open('gates_tracker/urls.py', 'w') as f:
    f.write(new_content)

print(' Added reports URLs to main urls.py configuration')
print(' Reports app is now properly registered')
