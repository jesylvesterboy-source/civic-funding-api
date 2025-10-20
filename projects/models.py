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

    # Financial Information
    currency = models.CharField(max_length=10, default='USD', blank=True, null=True)
    donor = models.CharField(max_length=200, blank=True, null=True)
    implementing_partner = models.CharField(max_length=200, blank=True, null=True)

    # Project Management - ROBUST VERSION
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='managed_projects')
    # ESSENTIAL ROBUST FIELD: Project Manager for accountability
    project_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='project_managed_projects', verbose_name='Project Manager',
                                        help_text='Primary accountable person for project delivery')
    is_active = models.BooleanField(default=True)
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                                default='medium')
    requires_approval = models.BooleanField(default=True)

    # Timeline Tracking
    actual_start_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)

    # Risk Management - ROBUST VERSION
    risk_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                                  default='medium')
    risks = models.TextField(blank=True, null=True, help_text='List of identified risks')
    # ESSENTIAL ROBUST FIELD: Detailed risk assessment notes
    risk_notes = models.TextField(blank=True, null=True, verbose_name='Risk Assessment Notes',
                                  help_text='Detailed risk analysis, mitigation strategies, and contingency plans')
    objectives = models.TextField(blank=True, null=True)
    success_criteria = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text='Comma-separated tags')

    class Meta:
        db_table = 'projects_project'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-start_date', 'name']
        indexes = [
            models.Index(fields=['status', 'start_date']),
            models.Index(fields=['start_date']),
            models.Index(fields=['country']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('project-detail', kwargs={'pk': self.pk})

    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_active_status(self):
        return self.status == 'active'

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None
