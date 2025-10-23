# Enable delete in finances admin
with open('finances/admin.py', 'w') as f:
    f.write('''
from django.contrib import admin
from .models import Budget, Expense, FinancialReport

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    actions = ['delete_selected']

@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    actions = ['delete_selected']
''')

print(' Enabled delete in finances admin')
