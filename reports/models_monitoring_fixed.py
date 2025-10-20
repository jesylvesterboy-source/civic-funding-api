from django.db import models
from django.conf import settings
from core.models import TimeStampedModel, AutoExportMixin
from projects.models import Project
from django.utils import timezone

class MonitoringVisit(TimeStampedModel, AutoExportMixin):
    """Tracks monitoring and evaluation visits for accountability."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField(default=timezone.now)
    visited_by = models.CharField(max_length=150, default='Field Officer')
    purpose = models.CharField(max_length=250, default='Routine Monitoring')
    findings = models.TextField(default='Initial assessment in progress')
    recommendations = models.TextField(blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)
    next_visit_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Monitoring Visit - {self.project.name} - {self.visit_date}"
