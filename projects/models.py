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
        'Export projects to CSV - ultra robust version'
        import csv
        from django.http import HttpResponse
        
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'

            writer = csv.writer(response)
            writer.writerow(['Name', 'Code', 'Description', 'Budget', 'Status', 'Progress', 'Start Date', 'End Date'])

            # Safely get all projects
            projects = cls.objects.all()
            
            for project in projects:
                try:
                    # Use extremely safe attribute access
                    name = getattr(project, 'name', 'N/A')
                    code = getattr(project, 'code', 'N/A')
                    description = getattr(project, 'description', '') or ''
                    budget = getattr(project, 'budget', 0) or 0
                    status = getattr(project, 'status', 'unknown')
                    progress = getattr(project, 'progress', 0) or 0
                    
                    # Handle date fields safely
                    start_date = getattr(project, 'start_date', '')
                    if start_date:
                        start_date = str(start_date)
                    else:
                        start_date = ''
                        
                    end_date = getattr(project, 'end_date', '')
                    if end_date:
                        end_date = str(end_date)
                    else:
                        end_date = ''

                    writer.writerow([
                        name, code, description, budget, status, progress, start_date, end_date
                    ])
                except Exception as e:
                    # If individual project fails, skip it and continue
                    print(f"Error exporting project {getattr(project, 'id', 'unknown')}: {e}")
                    continue

            return response
            
        except Exception as e:
            # If everything fails, return a basic error response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'
            writer = csv.writer(response)
            writer.writerow(['Error', 'Message'])
            writer.writerow(['Export Failed', str(e)])
            return response

    @classmethod
    def export_to_excel(cls):
        'Export projects to Excel - ultra robust version'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        try:
            data = []
            projects = cls.objects.all()
            
            for project in projects:
                try:
                    # Use extremely safe attribute access
                    name = getattr(project, 'name', 'N/A')
                    code = getattr(project, 'code', 'N/A')
                    description = getattr(project, 'description', '') or ''
                    budget = float(getattr(project, 'budget', 0) or 0)
                    status = getattr(project, 'status', 'unknown')
                    progress = getattr(project, 'progress', 0) or 0
                    
                    # Handle date fields safely
                    start_date = getattr(project, 'start_date', '')
                    if start_date:
                        start_date = str(start_date)
                    else:
                        start_date = ''
                        
                    end_date = getattr(project, 'end_date', '')
                    if end_date:
                        end_date = str(end_date)
                    else:
                        end_date = ''

                    data.append({
                        'Name': name,
                        'Code': code,
                        'Description': description,
                        'Budget': budget,
                        'Status': status,
                        'Progress': progress,
                        'Start Date': start_date,
                        'End Date': end_date
                    })
                except Exception as e:
                    print(f"Error exporting project {getattr(project, 'id', 'unknown')}: {e}")
                    continue

            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Projects', index=False)

            response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=\"projects.xlsx\"'
            return response
            
        except Exception as e:
            # If everything fails, return a basic error Excel file
            output = BytesIO()
            df = pd.DataFrame([{'Error': 'Export Failed', 'Message': str(e)}])
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Error', index=False)
                
            response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=\"projects_error.xlsx\"'
            return response

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
