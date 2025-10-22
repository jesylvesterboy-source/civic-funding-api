# Read the dashboard template
with open('dashboard/templates/dashboard/home.html', 'r') as f:
    content = f.read()

# Replace reports_main with reports:reports_main
old_reference = "{% url 'reports_main' %}"
new_reference = "{% url 'reports:reports_main' %}"
content = content.replace(old_reference, new_reference)

# Write back to file
with open('dashboard/templates/dashboard/home.html', 'w') as f:
    f.write(content)

print(' Fixed dashboard template - updated reports_main to reports:reports_main')
print(' The template now uses the correct namespace')
