from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from core.models import TimeStampedModel
from projects.models import Project


class Budget(TimeStampedModel):
    """Project budget allocation and tracking."""
    
    BUDGET_TYPES = [
        ('personnel', 'Personnel'),
        ('equipment', 'Equipment'),
        ('training', 'Training'),
        ('logistics', 'Logistics'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES)
    description = models.TextField()
    allocated_amount = models.DecimalField(
        max_digits=14, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        unique_together = ['project', 'budget_type']
    
    def __str__(self):
        return f"{self.project.name} - {self.get_budget_type_display()} (${self.allocated_amount})"
    
    @property
    def total_expenses(self):
        """Calculate total expenses for this budget."""
        return sum(expense.amount for expense in self.expenses.all())
    
    @property
    def remaining_amount(self):
        """Calculate remaining budget amount."""
        return self.allocated_amount - self.total_expenses
    
    @property
    def utilization_percentage(self):
        """Calculate budget utilization percentage."""
        if self.allocated_amount == 0:
            return 0
        return (self.total_expenses / self.allocated_amount) * 100


class Expense(TimeStampedModel):
    """Track actual expenses against budgets."""
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('cheque', 'Cheque'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    description = models.TextField()
    amount = models.DecimalField(
        max_digits=14, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    expense_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='bank_transfer')
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='approved_expenses'
    )
    paid_by = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-expense_date']
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
    
    def __str__(self):
        return f"{self.budget.project.name} - ${self.amount} - {self.expense_date}"


class FinancialReport(TimeStampedModel):
    """Consolidated financial reports."""
    
    REPORT_PERIODS = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
        ('special', 'Special Report'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='financial_reports')
    report_period = models.CharField(max_length=20, choices=REPORT_PERIODS)
    period_start = models.DateField()
    period_end = models.DateField()
    total_budget = models.DecimalField(max_digits=14, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=14, decimal_places=2)
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notes = models.TextField(blank=True, null=True)
    is_finalized = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-period_end']
        verbose_name = "Financial Report"
        verbose_name_plural = "Financial Reports"
    
    def __str__(self):
        return f"{self.project.name} - {self.get_report_period_display()} - {self.period_end}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate balance before saving."""
        self.balance = self.total_budget - self.total_expenses
        super().save(*args, **kwargs)