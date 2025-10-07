from django.contrib import admin
from .models import Budget, Expense, FinancialReport

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = [
        'project', 'budget_type', 'allocated_amount', 
        'total_expenses', 'remaining_amount', 'start_date', 'end_date'
    ]
    list_filter = ['budget_type', 'start_date', 'project']
    search_fields = ['project__name', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['total_expenses', 'remaining_amount']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
        'budget', 'description_short', 'amount', 'expense_date', 
        'payment_method', 'status', 'approved_by'
    ]
    list_filter = ['status', 'payment_method', 'expense_date', 'budget__project']
    search_fields = ['budget__project__name', 'description', 'receipt_number']
    date_hierarchy = 'expense_date'
    list_editable = ['status']
    
    def description_short(self, obj):
        """Display shortened description."""
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = [
        'project', 'report_period', 'period_start', 'period_end',
        'total_budget', 'total_expenses', 'balance', 'is_finalized'
    ]
    list_filter = ['report_period', 'period_end', 'is_finalized', 'project']
    search_fields = ['project__name', 'notes']
    date_hierarchy = 'period_end'
    readonly_fields = ['balance']