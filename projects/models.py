from django.db import models
from django.conf import settings
from django.utils import timezone
from core.models import TimeStampedModel
from core.export_import import CustomExportMixin

class Project(TimeStampedModel, CustomExportMixin):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # === CORE FIELDS (Always exist) ===
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    progress = models.PositiveIntegerField(default=0, help_text='Progress percentage (0-100)')

    # === ROBUST FIELDS (May exist in some databases) ===
    # Geographic Information
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    gps_coordinates = models.CharField(max_length=100, blank=True, null=True)
    
    # Financial Details
    currency = models.CharField(max_length=10, default='USD', blank=True, null=True)
    donor = models.CharField(max_length=200, blank=True, null=True)
    implementing_partner = models.CharField(max_length=200, blank=True, null=True)
    
    # Project Management
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects')
    is_active = models.BooleanField(default=True)
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    requires_approval = models.BooleanField(default=True)
    
    # Timeline Extensions
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    
    # Risk Management
    risk_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    risks = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    success_criteria = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Categorization
    tags = models.CharField(max_length=500, blank=True, null=True, help_text='Comma-separated tags')

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
        'Export projects to CSV - Only real data, no samples'
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'
        writer = csv.writer(response)
        
        # Professional headers
        headers = ['Project Name', 'Project Code', 'Description', 'Budget', 'Status', 'Progress', 'Start Date', 'End Date']
        writer.writerow(headers)

        # Export ONLY real projects - no sample data
        projects = cls.objects.all()
        
        for project in projects:
            writer.writerow([
                project.name,
                project.code,
                project.description or '',
                project.budget or 0,
                project.status,
                project.progress or 0,
                project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                project.end_date.strftime('%Y-%m-%d') if project.end_date else ''
            ])

        # If no projects, CSV will only have headers - professional and honest
        return response

    @classmethod
    def export_to_excel(cls):
        'Export projects to Excel - Only real data'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO

        data = []
        projects = cls.objects.all()
        
        # Export ONLY real projects
        for project in projects:
            data.append({
                'Project Name': project.name,
                'Project Code': project.code,
                'Description': project.description or '',
                'Budget': float(project.budget or 0),
                'Status': project.status,
                'Progress': project.progress or 0,
                'Start Date': project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                'End Date': project.end_date.strftime('%Y-%m-%d') if project.end_date else ''
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
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['country', 'region']),
        ]
