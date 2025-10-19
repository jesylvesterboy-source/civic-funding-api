from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from core.export_import import CustomExportMixin
from projects.models import Project

class Budget(TimeStampedModel, CustomExportMixin):
    BUDGET_TYPES = [
        ('operational', 'Operational'),
        ('capital', 'Capital'),
        ('personnel', 'Personnel'),
        ('training', 'Training'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]

    # Core Information
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=200)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES, default='operational')
    category = models.CharField(max_length=100, default='other')
    
    # Financial Details
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Management
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_budgets')
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_budgets')
    approved_date = models.DateTimeField(blank=True, null=True)
    
    # Tracking
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.project.code} - {self.name} - {self.budget_type}'

    @property
    def utilized_amount(self):
        'Calculate utilized amount from expenses'
        return self.expenses.aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def utilization_rate(self):
        'Calculate budget utilization rate'
        return (self.utilized_amount / self.allocated_amount * 100) if self.allocated_amount else 0

    @property
    def remaining_amount(self):
        'Calculate remaining budget'
        return self.allocated_amount - self.utilized_amount

    @property
    def is_active(self):
        'Check if budget is within its active period'
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    @classmethod
    def export_to_csv(cls):
        'Export budgets to CSV'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"budgets.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(['Project', 'Name', 'Budget Type', 'Category', 'Allocated Amount', 'Start Date', 'End Date', 'Utilization Rate'])
        
        for budget in cls.objects.all():
            writer.writerow([
                budget.project.code,
                budget.name,
                budget.budget_type,
                budget.category,
                budget.allocated_amount,
                budget.start_date,
                budget.end_date,
                f'{budget.utilization_rate:.1f}%'
            ])
        
        return response

    @classmethod
    def export_to_excel(cls):
        'Export budgets to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        data = []
        for budget in cls.objects.all():
            data.append({
                'Project': budget.project.code,
                'Name': budget.name,
                'Budget Type': budget.budget_type,
                'Category': budget.category,
                'Allocated Amount': budget.allocated_amount,
                'Start Date': budget.start_date,
                'End Date': budget.end_date,
                'Utilization Rate': f'{budget.utilization_rate:.1f}%'
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Budgets', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"budgets.xlsx\"'
        return response

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        unique_together = ['project', 'name']

class Expense(TimeStampedModel, CustomExportMixin):
    CATEGORY_CHOICES = [
        ('personnel', 'Personnel'),
        ('equipment', 'Equipment'),
        ('training', 'Training'),
        ('inputs', 'Farm Inputs'),
        ('transport', 'Transport'),
        ('administration', 'Administration'),
        ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('mobile_money', 'Mobile Money'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]

    # Core Information
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    
    # Expense Details
    description = models.TextField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    
    # Payment Information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    paid_to = models.CharField(max_length=200, blank=True, null=True)
    
    # Approval Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='submitted_expenses')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    approved_date = models.DateTimeField(blank=True, null=True)
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='paid_expenses')
    payment_date = models.DateTimeField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to='expense_attachments/', blank=True, null=True)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.project.code} - {self.description} - {self.amount}'

    @property
    def is_approved(self):
        return self.status == 'approved'

    @property
    def is_paid(self):
        return self.status == 'paid'

    @classmethod
    def export_to_csv(cls):
        'Export expenses to CSV'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"expenses.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(['Project', 'Budget', 'Description', 'Amount', 'Date', 'Category', 'Payment Method', 'Status', 'Receipt Number'])
        
        for expense in cls.objects.all():
            writer.writerow([
                expense.project.code,
                expense.budget.name,
                expense.description[:100],
                expense.amount,
                expense.date,
                expense.category,
                expense.payment_method,
                expense.status,
                expense.receipt_number or ''
            ])
        
        return response

    @classmethod
    def export_to_excel(cls):
        'Export expenses to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        data = []
        for expense in cls.objects.all():
            data.append({
                'Project': expense.project.code,
                'Budget': expense.budget.name,
                'Description': expense.description[:100],
                'Amount': expense.amount,
                'Date': expense.date,
                'Category': expense.category,
                'Payment Method': expense.payment_method,
                'Status': expense.status,
                'Receipt Number': expense.receipt_number or ''
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Expenses', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"expenses.xlsx\"'
        return response

    def save(self, *args, **kwargs):
        # Auto-set submitted_by if not set and creating
        if not self.pk and not self.submitted_by:
            # This would typically be set by the view, but as fallback
            pass
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        indexes = [
            models.Index(fields=['project', 'date']),
            models.Index(fields=['status', 'category']),
            models.Index(fields=['budget', 'date']),
        ]

class FinancialReport(TimeStampedModel, CustomExportMixin):
    REPORT_TYPES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('project', 'Project Report'),
        ('audit', 'Audit Report'),
    ]

    # Core Information
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='financial_reports')
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    report_period = models.CharField(max_length=50, help_text='e.g., January 2024, Q1 2024')
    
    # Timeline
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Financial Summary
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_position = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Content
    summary = models.TextField()
    key_findings = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Management
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='prepared_reports')
    is_finalized = models.BooleanField(default=False)
    finalized_date = models.DateTimeField(blank=True, null=True)
    
    # Attachments
    attachments = models.FileField(upload_to='financial_reports/', blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.project.code}'

    def save(self, *args, **kwargs):
        # Automatically calculate balance and net position
        self.balance = self.total_budget - self.total_expenses
        self.net_position = self.total_income - self.total_expenses
        super().save(*args, **kwargs)

    @property
    def profit_margin(self):
        'Calculate profit margin percentage'
        if self.total_income > 0:
            return (self.net_position / self.total_income * 100)
        return 0

    @property
    def budget_utilization_rate(self):
        'Calculate budget utilization rate'
        if self.total_budget > 0:
            return (self.total_expenses / self.total_budget * 100)
        return 0

    @classmethod
    def export_to_csv(cls):
        'Export financial reports to CSV'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"financial_reports.csv\"'
        
        writer = csv.writer(response)
        writer.writerow(['Project', 'Title', 'Report Type', 'Period', 'Total Budget', 'Total Income', 'Total Expenses', 'Net Position', 'Profit Margin'])
        
        for report in cls.objects.all():
            writer.writerow([
                report.project.code,
                report.title,
                report.report_type,
                report.report_period,
                report.total_budget,
                report.total_income,
                report.total_expenses,
                report.net_position,
                f'{report.profit_margin:.1f}%'
            ])
        
        return response

    @classmethod
    def export_to_excel(cls):
        'Export financial reports to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        data = []
        for report in cls.objects.all():
            data.append({
                'Project': report.project.code,
                'Title': report.title,
                'Report Type': report.report_type,
                'Period': report.report_period,
                'Total Budget': report.total_budget,
                'Total Income': report.total_income,
                'Total Expenses': report.total_expenses,
                'Net Position': report.net_position,
                'Profit Margin': f'{report.profit_margin:.1f}%'
            })
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Financial Reports', index=False)
        
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"financial_reports.xlsx\"'
        return response

    class Meta:
        ordering = ['-period_end', '-created_at']
        verbose_name = 'Financial Report'
        verbose_name_plural = 'Financial Reports'
        indexes = [
            models.Index(fields=['project', 'report_type']),
            models.Index(fields=['period_start', 'period_end']),
        ]
