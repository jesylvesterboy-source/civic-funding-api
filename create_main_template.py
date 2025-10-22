content = """{% extends "base.html" %}

{% block title %}Reports - FSSS{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <h1><i class="fas fa-chart-bar"></i> Reports Dashboard</h1>
            <p class="lead">Professional reporting and analytics</p>
            
            <div class="row">
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Financial Reports</h5>
                            <p class="card-text">Budget, expenses, and financial analytics</p>
                            <a href="{% url 'reports:financial_reports' %}" class="btn btn-primary">View Financial Reports</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Project Reports</h5>
                            <p class="card-text">Progress, milestones, and impact metrics</p>
                            <a href="{% url 'reports:project_reports' %}" class="btn btn-primary">View Project Reports</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

with open('reports/templates/reports/main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(' Created reports/main.html template')
