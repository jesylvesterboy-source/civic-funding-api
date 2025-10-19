from django.db import models
from core.models import TimeStampedModel, AutoExportMixin
from projects.models import Project
from farmers.models import Farmer


class PerformanceIndicator(TimeStampedModel, AutoExportMixin):
    """Tracks measurable indicators for project performance and impact."""

    CATEGORY_CHOICES = [
        ('yield', 'Crop Yield'),
        ('income', 'Household Income'),
        ('training', 'Training Participation'),
        ('adoption', 'Technology Adoption'),
        ('nutrition', 'Nutrition & Health'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='indicators')
    farmer = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True, blank=True, related_name='indicators')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(help_text="Detailed explanation of the indicator being tracked.")
    baseline_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Initial measurement before intervention.")
    current_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Latest measurement after intervention.")
    target_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Planned or expected target value.")
    measurement_date = models.DateField()

    class Meta:
        ordering = ['-measurement_date']
        verbose_name = "Performance Indicator"
        verbose_name_plural = "Performance Indicators"

    def __str__(self):
        return f"{self.project.name} - {self.category} ({self.measurement_date})"

    @property
    def progress_percentage(self):
        """Returns the percentage of progress made toward the target value."""
        try:
            return round((self.current_value / self.target_value) * 100, 2)
        except (ZeroDivisionError, TypeError):
            return 0.0
