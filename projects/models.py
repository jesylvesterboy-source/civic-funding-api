from django.db import models
from django.conf import settings  # Add this import
from core.models import TimeStampedModel


class Project(TimeStampedModel):
    """Represents a funded agricultural development project."""

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Unique project identifier or code.")
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2)
    donor = models.CharField(max_length=150, default="Bill & Melinda Gates Foundation")
    implementing_partner = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=100, default="Nigeria")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')

    # ✅ ADDED: Project manager relationship
    project_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='managed_projects',
        null=True,
        blank=True,
        help_text="User responsible for managing this project"
    )

    # Optional: progress tracking
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Completion progress in percentage")

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def duration(self):
        """Calculate project duration in days."""
        if self.end_date and self.start_date:
            return (self.end_date - self.start_date).days
        return None

    @property
    def is_active(self):
        """Check if project is currently active."""
        return self.status == 'ongoing'

    @property
    def budget_remaining(self):
        """Calculate remaining budget (placeholder for future financial integration)."""
        # This can be enhanced later when financial models are added
        return self.budget