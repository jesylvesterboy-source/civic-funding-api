import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from finances.models import Budget, Expense, FinancialReport
from projects.models import Project

User = get_user_model()

# =====================================================
# FINANCES API TESTS
# =====================================================
@pytest.mark.django_db
class TestFinancesAPI:
    def test_budget_list_authenticated(self, client, admin_user):
        """Ensure admin can view list of budgets."""
        client.force_login(admin_user)
        url = reverse('budget-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_create_budget(self, client, admin_user):
        """Ensure authenticated user can create a new budget."""
        client.force_login(admin_user)
        project = Project.objects.create(
            name="Test Project",
            code="TEST001",
            budget=100000,
            start_date="2025-01-01"
        )
        url = reverse('budget-list')
        data = {
            'project': project.id,
            'budget_type': 'personnel',
            'description': 'Test budget',
            'allocated_amount': 50000,
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'created_by': admin_user.id
        }
        response = client.post(url, data)
        assert response.status_code == 201
        assert Budget.objects.count() == 1

    def test_expense_approval_permission(self, client, finance_officer):
        """Ensure finance officer cannot approve expense without permission."""
        client.force_login(finance_officer)
        project = Project.objects.create(
            name="Test",
            code="TEST",
            budget=100000,
            start_date="2025-01-01"
        )
        budget = Budget.objects.create(
            project=project,
            budget_type='personnel',
            allocated_amount=50000,
            start_date='2025-01-01',
            end_date='2025-12-31',
            created_by=finance_officer
        )
        expense = Expense.objects.create(
            budget=budget,
            description='Test expense',
            amount=1000,
            expense_date='2025-01-15'
        )
        url = reverse('expense-approve', kwargs={'pk': expense.id})
        response = client.post(url)
        assert response.status_code == 403  # Expected: No approval permission


# =====================================================
# FINANCIAL CALCULATION TESTS
# =====================================================
@pytest.mark.django_db
class TestFinancialCalculations:
    def test_budget_utilization(self):
        """Test correct budget utilization calculation."""
        project = Project.objects.create(
            name="Test Project",
            code="TEST002",
            budget=100000,
            start_date="2025-01-01"
        )
        user = User.objects.create_user('test_user', 'test@example.com', 'password123')

        budget = Budget.objects.create(
            project=project,
            budget_type='personnel',
            allocated_amount=50000,
            start_date='2025-01-01',
            end_date='2025-12-31',
            created_by=user
        )

        # Create expenses
        Expense.objects.create(budget=budget, amount=10000, expense_date='2025-01-15')
        Expense.objects.create(budget=budget, amount=15000, expense_date='2025-02-15')

        # Assertions
        assert budget.total_expenses == 25000
        assert budget.remaining_amount == 25000
        assert round(budget.utilization_percentage, 1) == 50.0
