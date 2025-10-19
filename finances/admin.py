from django.contrib import admin
from .models import Budget, Expense, FinancialReport

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = [
        'project', 'category', 'allocated_amount', 'description'
    ]
    list_filter = ['category', 'created_at', 'project']
    search_fields = ['project__name', 'description']
    date_hierarchy = 'created_at'

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
        'project', 'budget', 'description_short', 'amount', 'date', 'category', 'receipt_number'
    ]
    list_filter = ['category', 'date', 'budget__project']
    search_fields = ['project__name', 'description', 'receipt_number']
    date_hierarchy = 'date'

    def description_short(self, obj):
        'Display shortened description.'
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'report_type', 'period_start', 'period_end',
        'total_income', 'total_expenses', 'net_position'
    ]
    list_filter = ['report_type', 'period_end']
    search_fields = ['title', 'summary']
    date_hierarchy = 'period_end'
