clean_content = """from django.shortcuts import render

# Create your views here.

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

with open('reports/views.py', 'w', encoding='utf-8') as f:
    f.write(clean_content)

print(' Created clean reports/views.py without duplicates')
