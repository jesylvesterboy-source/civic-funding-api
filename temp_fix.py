# Read current content
with open('reports/views.py', 'r') as f:
    content = f.read()

# Add the required functions
new_content = content + """

def reports_main(request):
    \"\"\"Main reports landing page\"\"\"
    return render(request, 'reports/main.html')

def reports_dashboard(request):
    \"\"\"Reports dashboard page\"\"\"
    return render(request, 'reports/dashboard.html')

def financial_reports(request):
    \"\"\"Financial reports page\"\"\"
    return render(request, 'reports/financial.html')

def project_reports(request):
    \"\"\"Project reports page\"\"\"
    return render(request, 'reports/projects.html')
"""

# Write back to file
with open('reports/views.py', 'w') as f:
    f.write(new_content)

print(' Added missing view functions to reports/views.py')
