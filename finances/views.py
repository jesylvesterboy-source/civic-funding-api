from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Budget, Expense, FinancialReport

@api_view(['GET'])
@login_required
def financial_dashboard(request):
    """Comprehensive financial dashboard data"""
    
    # Date ranges
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Budget statistics
    total_budgets = Budget.objects.count()
    total_allocated = Budget.objects.aggregate(Sum('allocated_amount'))['allocated_amount__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Budget utilization by type
    budget_utilization = Budget.objects.annotate(
        expenses_total=Sum('expenses__amount')
    ).values('budget_type').annotate(
        allocated=Sum('allocated_amount'),
        spent=Sum('expenses__amount'),
        utilization=Sum('expenses__amount') * 100 / Sum('allocated_amount')
    )
    
    # Recent expenses
    recent_expenses = Expense.objects.select_related(
        'budget__project'
    ).order_by('-expense_date')[:10]
    
    # Monthly spending trend
    monthly_spending = Expense.objects.filter(
        expense_date__gte=thirty_days_ago
    ).extra(
        {'month': "date_trunc('month', expense_date)"}
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('month')
    
    dashboard_data = {
        'summary': {
            'total_budgets': total_budgets,
            'total_allocated': float(total_allocated),
            'total_expenses': float(total_expenses),
            'remaining_budget': float(total_allocated - total_expenses),
            'overall_utilization': (total_expenses / total_allocated * 100) if total_allocated > 0 else 0,
        },
        'budget_utilization': list(budget_utilization),
        'monthly_trend': list(monthly_spending),
        'recent_expenses': [
            {
                'project': exp.budget.project.name,
                'description': exp.description,
                'amount': float(exp.amount),
                'date': exp.expense_date.isoformat(),
                'status': exp.status
            }
            for exp in recent_expenses
        ]
    }
    
    return Response(dashboard_data)

@api_view(['GET'])
@login_required
def project_financial_summary(request, project_id):
    """Financial summary for a specific project"""
    budgets = Budget.objects.filter(project_id=project_id).annotate(
        expenses_total=Sum('expenses__amount')
    )
    
    project_data = {
        'budgets': [
            {
                'type': budget.get_budget_type_display(),
                'allocated': float(budget.allocated_amount),
                'spent': float(budget.expenses_total or 0),
                'remaining': float(budget.allocated_amount - (budget.expenses_total or 0)),
                'utilization': ((budget.expenses_total or 0) / budget.allocated_amount * 100) if budget.allocated_amount > 0 else 0
            }
            for budget in budgets
        ]
    }
    
    return Response(project_data)