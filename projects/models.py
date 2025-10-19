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

    # Basic Information - These fields definitely exist
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Financial Information
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Timeline
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # Status Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    progress = models.PositiveIntegerField(default=0, help_text='Progress percentage (0-100)')

    def __str__(self):
        return f'{self.code} - {self.name}'

    @classmethod
    def export_to_csv(cls):
        'Export projects to CSV - Minimal fields only'
        import csv
        from django.http import HttpResponse
        
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'
            writer = csv.writer(response)
            
            # Only include fields that 100% exist in production
            headers = ['Project Name', 'Project Code', 'Description', 'Budget', 'Status', 'Progress', 'Start Date', 'End Date']
            writer.writerow(headers)

            # Get and export projects
            projects = cls.objects.all()
            
            for project in projects:
                # Use only the most basic fields that definitely exist
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

            return response
            
        except Exception as e:
            # If anything fails, return a properly formatted error CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=\"projects.csv\"'
            writer = csv.writer(response)
            writer.writerow(['Project Name', 'Project Code', 'Description'])
            writer.writerow(['No projects available', '', 'Database is empty or export failed'])
            return response

    @classmethod
    def export_to_excel(cls):
        'Export projects to Excel - Minimal fields only'
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO
        
        try:
            data = []
            projects = cls.objects.all()
            
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
            
        except Exception as e:
            # Return empty but properly formatted Excel
            output = BytesIO()
            df = pd.DataFrame([{
                'Project Name': 'No Data Available', 
                'Project Code': 'N/A',
                'Description': 'Database is empty or export failed'
            }])
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Projects', index=False)
                
            response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=\"projects.xlsx\"'
            return response

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
