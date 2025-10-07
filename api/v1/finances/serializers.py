from rest_framework import serializers
from finances.models import Budget, Expense, FinancialReport

class BudgetSerializer(serializers.ModelSerializer):
    total_expenses = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    utilization_percentage = serializers.ReadOnlyField()
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExpenseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='budget.project.name', read_only=True)
    budget_type = serializers.CharField(source='budget.budget_type', read_only=True)
    
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class FinancialReportSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    utilization_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = FinancialReport
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'balance']