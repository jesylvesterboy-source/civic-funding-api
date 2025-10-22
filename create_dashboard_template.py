content = """{% extends "base.html" %}

{% block title %}Reports Analytics - FSSS{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1><i class="fas fa-analytics"></i> Reports Analytics</h1>
    <p>Comprehensive reporting dashboard with charts and analytics.</p>
    <div class="alert alert-info">
        <strong>Note:</strong> This is the reports dashboard page. Detailed analytics will be added in Phase 5.
    </div>
</div>
{% endblock %}
"""

with open('reports/templates/reports/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Created reports/dashboard.html template')
