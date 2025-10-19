from rest_framework import viewsets
from ..models import Budget, Expense, FinancialReport
from .serializers import BudgetSerializer, ExpenseSerializer, FinancialReportSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
