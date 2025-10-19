from django.db import models
from core.models import TimeStampedModel
from core.export_import import ExportImportMixin
from projects.models import Project

class Location(TimeStampedModel, ExportImportMixin):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Nigeria')

    def __str__(self):
        return f'{self.name}, {self.district}'

class Household(TimeStampedModel, ExportImportMixin):
    head_of_household = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    family_size = models.PositiveIntegerField(default=1)
    income_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='low')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='households')

    def __str__(self):
        return self.head_of_household

class Farmer(TimeStampedModel, ExportImportMixin):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    education_level = models.CharField(max_length=50, blank=True, null=True)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='farmers')
    projects = models.ManyToManyField(Project, related_name='farmers', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        # Calculate farmer age
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

class FarmPlot(TimeStampedModel, ExportImportMixin):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farm_plots')
    size_acres = models.DecimalField(max_digits=8, decimal_places=2)
    soil_type = models.CharField(max_length=50, blank=True, null=True)
    gps_coordinates = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='farm_plots', null=True, blank=True)

    def __str__(self):
        return f'{self.farmer} plot ({self.size_acres} acres)'
