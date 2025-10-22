content = """{% extends "base.html" %}

{% block title %}Project Reports - FSSS{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1><i class="fas fa-tasks"></i> Project Reports</h1>
    <p>Project progress, milestones, and impact measurement reports.</p>
    <div class="alert alert-info">
        <strong>Project Reports Features:</strong> Progress tracking, milestone completion, impact metrics, and performance analytics.
    </div>
</div>
{% endblock %}
"""

with open('reports/templates/reports/projects.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Created reports/projects.html template')
