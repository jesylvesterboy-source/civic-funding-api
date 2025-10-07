from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from finances.models import Budget, Expense, FinancialReport
from .serializers import BudgetSerializer, ExpenseSerializer, FinancialReportSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'budget_type', 'start_date']
    
    def get_queryset(self):
        return Budget.objects.select_related('project', 'created_by').prefetch_related('expenses')
    
    @action(detail=True, methods=['get'])
    def expenses(self, request, pk=None):
        budget = self.get_object()
        expenses = budget.expenses.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['budget', 'status', 'payment_method', 'expense_date']
    
    def get_queryset(self):
        return Expense.objects.select_related('budget__project', 'approved_by')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        expense = self.get_object()
        if not request.user.can_approve_budgets:
            return Response(
                {'error': 'You do not have permission to approve expenses'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        expense.status = 'approved'
        expense.approved_by = request.user
        expense.save()
        return Response({'status': 'expense approved'})

class FinancialReportViewSet(viewsets.ModelViewSet):
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'report_period', 'is_finalized']
    
    def get_queryset(self):
        return FinancialReport.objects.select_related('project', 'prepared_by')