from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from core.export_import import ExportImportMixin

class Project(TimeStampedModel, ExportImportMixin):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    objectives = models.TextField(blank=True, null=True)
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField()
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    
    # Financials
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Stakeholders
    donor = models.CharField(max_length=200)
    implementing_partner = models.CharField(max_length=200)
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects')
    
    # Location
    country = models.CharField(max_length=100, default='Nigeria')
    region = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    gps_coordinates = models.CharField(max_length=100, blank=True, null=True)
    
    # Status & Progress
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    progress = models.IntegerField(default=0, help_text='Progress percentage (0-100)')
    
    # Risk Management
    risk_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    risk_notes = models.TextField(blank=True, null=True)
    
    # Additional Metadata
    tags = models.CharField(max_length=500, blank=True, null=True, help_text='Comma-separated tags for categorization')
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def duration_days(self):
        'Calculate project duration in days'
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0

    @property
    def budget_utilization(self):
        'Calculate budget utilization percentage'
        from finances.models import Expense
        total_expenses = Expense.objects.filter(project=self).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        return (total_expenses / self.budget * 100) if self.budget > 0 else 0

    @property
    def is_overdue(self):
        'Check if project is overdue'
        from django.utils import timezone
        return self.end_date < timezone.now().date() if self.end_date else False

    @property
    def days_remaining(self):
        'Calculate days remaining until project end'
        from django.utils import timezone
        if self.end_date:
            remaining = (self.end_date - timezone.now().date()).days
            return max(0, remaining)
        return 0

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['country', 'region']),
        ]
