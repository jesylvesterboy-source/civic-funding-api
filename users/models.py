from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('project_manager', 'Project Manager'),
        ('field_officer', 'Field Officer'),
        ('finance_officer', 'Finance Officer'),
        ('viewer', 'Viewer'),
    ]

    # Existing field
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer'
    )

    # *** NEW FIELDS ADDED TO FIX ADMIN ERRORS ***
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Phone Number' # Optional: for better admin display
    )

    organization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Organization'
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name='Is Verified'
    )
    # *********************************************

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"