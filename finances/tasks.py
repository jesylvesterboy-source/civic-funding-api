from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Budget, Expense
from core.email_service import send_budget_alert_notification

@shared_task
def check_budget_utilization():
    """Check budget utilization and send alerts"""
    budgets = Budget.objects.annotate(
        expenses_total=Sum('expenses__amount')
    ).filter(expenses_total__gt=0)
    
    for budget in budgets:
        utilization = budget.utilization_percentage
        
        # Send alerts at different thresholds
        if utilization >= 80:
            send_budget_alert_notification(budget, threshold=80)
        elif utilization >= 90:
            send_budget_alert_notification(budget, threshold=90)
        elif utilization >= 95:
            send_budget_alert_notification(budget, threshold=95)

@shared_task
def generate_monthly_financial_reports():
    """Generate monthly financial reports for all projects"""
    from .models import FinancialReport, Project
    
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    for project in Project.objects.all():
        total_budget = project.budgets.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
        total_expenses = Expense.objects.filter(
            budget__project=project,
            expense_date__range=[start_date, end_date]
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        FinancialReport.objects.create(
            project=project,
            report_period='monthly',
            period_start=start_date,
            period_end=end_date,
            total_budget=total_budget,
            total_expenses=total_expenses,
            prepared_by=project.project_manager or project.created_by,
            notes=f"Automated monthly report for {start_date} to {end_date}"
        )

@shared_task
def export_financial_data_async(user_email, export_type, filters):
    """Async task for large data exports"""
    # This would generate the export and email it to the user
    # Implementation depends on your specific export needs
    pass