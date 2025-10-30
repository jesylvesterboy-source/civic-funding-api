from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Department(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class EnterpriseUserProfile(TimeStampedModel):
    USER_ROLES = [
        ('admin', 'System Administrator'),
        ('manager', 'Department Manager'),
        ('supervisor', 'Team Supervisor'),
        ('field_agent', 'Field Agent'),
        ('analyst', 'Data Analyst'),
        ('viewer', 'Read-Only Viewer'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enterprise_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    role = models.CharField(max_length=20, choices=USER_ROLES)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_joining = models.DateField()
    is_active = models.BooleanField(default=True)
    permissions_level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    last_activity = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.get_full_name()} ({self.employee_id})'

class PerformanceCycle(TimeStampedModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class KPICategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    def __str__(self):
        return self.name

class StaffPerformance(TimeStampedModel):
    staff = models.ForeignKey(EnterpriseUserProfile, on_delete=models.CASCADE, related_name='performance_records')
    performance_cycle = models.ForeignKey(PerformanceCycle, on_delete=models.CASCADE)
    overall_score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    manager = models.ForeignKey(EnterpriseUserProfile, on_delete=models.CASCADE, related_name='managed_performances')
    evaluation_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved')])
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['staff', 'performance_cycle']

class PerformanceMetric(TimeStampedModel):
    performance = models.ForeignKey(StaffPerformance, on_delete=models.CASCADE, related_name='metrics')
    kpi_category = models.ForeignKey(KPICategory, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    evidence = models.TextField(blank=True)
    reviewer_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.kpi_category.name}: {self.score}'

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    population = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class CBOGroup(TimeStampedModel):
    GROUP_TYPES = [
        ('cooperative', 'Agricultural Cooperative'),
        ('association', 'Farmers Association'),
        ('savings', 'Savings Group'),
        ('training', 'Training Group'),
    ]
    
    name = models.CharField(max_length=200)
    group_id = models.CharField(max_length=20, unique=True)
    group_type = models.CharField(max_length=20, choices=GROUP_TYPES)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    established_date = models.DateField()
    total_members = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f'{self.name} ({self.group_id})'

class Farmer(TimeStampedModel):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    farmer_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    cbo_group = models.ForeignKey(CBOGroup, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    registration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    last_engagement_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.farmer_id})'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class DashboardSnapshot(TimeStampedModel):
    snapshot_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    snapshot_date = models.DateTimeField()
    metrics = models.JSONField()
    generated_by = models.ForeignKey(EnterpriseUserProfile, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f'Snapshot {self.snapshot_id} - {self.snapshot_date}'

class AuditLog(TimeStampedModel):
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('export', 'Export'),
    ]
    
    user = models.ForeignKey(EnterpriseUserProfile, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.user} - {self.action_type} - {self.model_name}'


