content = """{% extends "base.html" %}

{% block title %}Financial Reports - FSSS{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1><i class="fas fa-money-bill-wave"></i> Financial Reports</h1>
    <p>Budget, expense tracking, and financial analytics reports.</p>
    <div class="alert alert-info">
        <strong>Financial Reports Features:</strong> Budget analysis, expense tracking, financial statements, and compliance reports.
    </div>
</div>
{% endblock %}
"""

with open('reports/templates/reports/financial.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Created reports/financial.html template')
