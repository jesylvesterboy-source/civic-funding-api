from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from core.export_import import CustomExportMixin

class Project(TimeStampedModel, CustomExportMixin):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Financial Information
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Timeline
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    
    # Status Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    progress = models.PositiveIntegerField(default=0, help_text='Progress percentage (0-100)')
    
    # Management
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects')
    is_active = models.BooleanField(default=True)
    
    # Additional Information
    objectives = models.TextField(blank=True, null=True)
    success_criteria = models.TextField(blank=True, null=True)
    risks = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.code} - {self.name}'

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    @property
    def is_on_track(self):
        if not self.start_date or not self.end_date:
            return None
        today = timezone.now().date()
        total_days = self.duration_days
        if total_days and total_days > 0:
            elapsed_days = (today - self.start_date).days
            expected_progress = min(100, (elapsed_days / total_days) * 100)
            return self.progress >= expected_progress
        return None

    @property
    def time_remaining(self):
        if self.end_date:
            today = timezone.now().date()
            remaining = (self.end_date - today).days
            return max(0, remaining)
        return 0

    @classmethod
    def export_to_csv(cls):
        'Export projects to CSV'
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Code', 'Description', 'Budget', 'Status', 'Progress', 'Start Date', 'End Date'])

        for project in cls.objects.all():
            # Use safe attribute access with fallbacks
            writer.writerow([
                getattr(project, 'name', ''),
                getattr(project, 'code', ''),
                getattr(project, 'description', '') or '',
                getattr(project, 'budget', 0) or 0,
                getattr(project, 'status', ''),
                getattr(project, 'progress', 0) or 0,
                getattr(project, 'start_date', '') or '',
                getattr(project, 'end_date', '') or ''
            ])

        return response

    @classmethod
    def export_to_excel(cls):
        'Export projects to Excel'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO

        data = []
        for project in cls.objects.all():
            # Use safe attribute access with fallbacks
            data.append({
                'Name': getattr(project, 'name', ''),
                'Code': getattr(project, 'code', ''),
                'Description': getattr(project, 'description', '') or '',
                'Budget': float(getattr(project, 'budget', 0) or 0),
                'Status': getattr(project, 'status', ''),
                'Progress': getattr(project, 'progress', 0) or 0,
                'Start Date': str(getattr(project, 'start_date', '') or ''),
                'End Date': str(getattr(project, 'end_date', '') or '')
            })

        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Projects', index=False)

        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=\"projects.xlsx\"'
        return response

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
