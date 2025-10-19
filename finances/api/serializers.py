from rest_framework import serializers
from ..models import Budget, Expense, FinancialReport

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class FinancialReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialReport
        fields = '__all__'
