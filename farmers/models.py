from django.db import models
from django.conf import settings
from core.models import TimeStampedModel
from projects.models import Project

class Location(TimeStampedModel):
    """Represents geographical locations (villages, communities)."""
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Nigeria")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.district}"

class Household(TimeStampedModel):
    """Represents farmer households."""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='households')
    head_of_household = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    family_size = models.PositiveIntegerField(default=1)
    income_level = models.CharField(max_length=20, choices=[
        ('low', 'Low Income'),
        ('medium', 'Medium Income'),
        ('high', 'High Income'),
    ], default='low')
    
    class Meta:
        ordering = ['head_of_household']
    
    def __str__(self):
        return f"{self.head_of_household}'s Household"

class Farmer(TimeStampedModel):
    """Represents individual farmers."""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='farmers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    education_level = models.CharField(max_length=50, blank=True, null=True)
    projects = models.ManyToManyField(Project, related_name='farmers', blank=True)
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class FarmPlot(TimeStampedModel):
    """Represents farm plots belonging to farmers."""
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farm_plots')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    size_acres = models.DecimalField(max_digits=8, decimal_places=2)
    soil_type = models.CharField(max_length=50, blank=True, null=True)
    gps_coordinates = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.farmer.full_name}'s Plot ({self.size_acres} acres)"