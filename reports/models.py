from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from projects.models import Project  # Now this will work!


class MonitoringVisit(TimeStampedModel):
    """Tracks monitoring and evaluation visits for accountability."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField()
    visited_by = models.CharField(max_length=150)
    purpose = models.CharField(max_length=250)
    findings = models.TextField()
    recommendations = models.TextField(blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)
    next_visit_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-visit_date']
        verbose_name = "Monitoring Visit"
        verbose_name_plural = "Monitoring Visits"

    def __str__(self):
        return f"{self.project.name} visit on {self.visit_date}"


class Report(TimeStampedModel):
    """Consolidated project report combining performance, finance, and visit summaries."""

    REPORT_TYPE_CHOICES = [
        ('monthly', 'Monthly Report'),
        ('quarterly', 'Quarterly Report'),
        ('annual', 'Annual Report'),
        ('final', 'Final Report'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    reporting_period_start = models.DateField()
    reporting_period_end = models.DateField()
    summary = models.TextField(help_text="Narrative summary of project activities and progress.")
    
    # ✅ CORRECTED: Use settings.AUTH_USER_MODEL
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='submitted_reports'
    )
    
    submission_date = models.DateField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_reports'
    )

    class Meta:
        ordering = ['-reporting_period_end']
        verbose_name = "Project Report"
        verbose_name_plural = "Project Reports"

    def __str__(self):
        return f"{self.project.name} - {self.report_type} ({self.reporting_period_end.year})"