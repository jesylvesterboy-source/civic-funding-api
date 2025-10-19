from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from ..models import Budget, Expense, FinancialReport
from .serializers import BudgetSerializer, ExpenseSerializer, FinancialReportSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return Budget.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return Budget.export_to_excel()

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return Expense.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return Expense.export_to_excel()

class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return FinancialReport.export_to_csv()

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        return FinancialReport.export_to_excel()
