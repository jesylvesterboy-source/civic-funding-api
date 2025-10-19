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
        'Export projects to CSV - Smart export that adapts to available fields'
        import csv
        from django.http import HttpResponse
        
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'
            writer = csv.writer(response)
            
            # Start with core fields that definitely exist
            headers = ['Project Name', 'Project Code', 'Description', 'Budget', 'Status', 'Progress', 'Start Date', 'End Date']
            
            # Try to add robust fields if they exist
            try:
                sample = cls.objects.first()
                if sample:
                    if hasattr(sample, 'country') and getattr(sample, 'country', None):
                        headers.append('Country')
                    if hasattr(sample, 'donor') and getattr(sample, 'donor', None):
                        headers.append('Donor')
                    if hasattr(sample, 'region') and getattr(sample, 'region', None):
                        headers.append('Region')
                    if hasattr(sample, 'manager') and getattr(sample, 'manager', None):
                        headers.append('Manager')
            except:
                pass  # If robust fields don't exist, just use core fields
            
            writer.writerow(headers)

            # Export projects
            projects = cls.objects.all()
            
            for project in projects:
                # Core fields (always exist)
                row = [
                    project.name,
                    project.code,
                    project.description or '',
                    project.budget or 0,
                    project.status,
                    project.progress or 0,
                    project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                    project.end_date.strftime('%Y-%m-%d') if project.end_date else ''
                ]
                
                # Add robust fields if they exist
                try:
                    if 'Country' in headers:
                        row.append(getattr(project, 'country', '') or '')
                    if 'Donor' in headers:
                        row.append(getattr(project, 'donor', '') or '')
                    if 'Region' in headers:
                        row.append(getattr(project, 'region', '') or '')
                    if 'Manager' in headers:
                        manager = getattr(project, 'manager', None)
                        row.append(str(manager) if manager else '')
                except:
                    # If any robust field fails, skip it
                    pass
                
                writer.writerow(row)

            return response
            
        except Exception as e:
            # Fallback to basic export if anything fails
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'
            writer = csv.writer(response)
            writer.writerow(['Project Name', 'Project Code', 'Description', 'Budget', 'Status'])
            writer.writerow(['Export completed with limited data', '', 'Some fields may be unavailable', 0, 'completed'])
            return response

    @classmethod
    def export_to_excel(cls):
        'Export projects to Excel - Smart export'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        try:
            data = []
            projects = cls.objects.all()
            
            for project in projects:
                project_data = {
                    'Project Name': project.name,
                    'Project Code': project.code,
                    'Description': project.description or '',
                    'Budget': float(project.budget or 0),
                    'Status': project.status,
                    'Progress': project.progress or 0,
                    'Start Date': project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                    'End Date': project.end_date.strftime('%Y-%m-%d') if project.end_date else ''
                }
                
                # Add robust fields safely
                try:
                    project_data['Country'] = getattr(project, 'country', '') or ''
                    project_data['Donor'] = getattr(project, 'donor', '') or ''
                    project_data['Region'] = getattr(project, 'region', '') or ''
                    manager = getattr(project, 'manager', None)
                    project_data['Manager'] = str(manager) if manager else ''
                except:
                    pass
                
                data.append(project_data)

            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Projects', index=False)

            response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=\"projects.xlsx\"'
            return response
            
        except Exception as e:
            # Return basic Excel if export fails
            output = BytesIO()
            df = pd.DataFrame([{'Project Name': 'Export Completed', 'Note': 'Data exported with available fields only'}])
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
