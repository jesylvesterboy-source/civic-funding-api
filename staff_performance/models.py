# staff_performance/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import TimeStampedModel, UUIDModel

class StaffMember(TimeStampedModel, UUIDModel):
    """Comprehensive staff member profile with performance tracking"""
    
    DEPARTMENT_CHOICES = [
        ('field_operations', 'Field Operations'),
        ('grant_management', 'Grant Management'),
        ('farmer_support', 'Farmer Support'),
        ('monitoring_evaluation', 'Monitoring & Evaluation'),
        ('finance_admin', 'Finance & Administration'),
        ('technical_services', 'Technical Services'),
    ]
    
    POSITION_LEVELS = [
        ('entry', 'Entry Level'),
        ('officer', 'Field Officer'),
        ('supervisor', 'Supervisor'),
        ('manager', 'Manager'),
        ('director', 'Director'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        verbose_name='System User'
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Employee ID',
        help_text='Unique staff identification number'
    )
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        verbose_name='Department',
        help_text='Primary department assignment'
    )
    position_title = models.CharField(
        max_length=100,
        verbose_name='Position Title',
        help_text='Official job title'
    )
    position_level = models.CharField(
        max_length=20,
        choices=POSITION_LEVELS,
        verbose_name='Position Level'
    )
    hire_date = models.DateField(
        verbose_name='Hire Date',
        help_text='Date staff joined organization'
    )
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name='Direct Supervisor',
        help_text='Immediate supervisor for performance reviews'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active Status',
        help_text='Designates whether staff is currently active'
    )
    
    # Performance Metrics (Calculated)
    overall_performance_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Overall Performance Score',
        help_text='Aggregated performance score (0-100)'
    )
    last_performance_review = models.DateField(
        null=True,
        blank=True,
        verbose_name='Last Performance Review'
    )
    
    # Contact & Location
    work_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Work Phone'
    )
    work_email = models.EmailField(
        blank=True,
        verbose_name='Work Email'
    )
    assigned_region = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Assigned Region',
        help_text='Primary geographical area of responsibility'
    )
    
    class Meta:
        db_table = 'staff_performance_staffmember'
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'
        ordering = ['department', 'position_level', 'user__last_name']
        indexes = [
            models.Index(fields=['department', 'is_active']),
            models.Index(fields=['position_level']),
            models.Index(fields=['overall_performance_score']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position_title}"
    
    @property
    def full_name(self):
        return self.user.get_full_name()
    
    @property
    def tenure_months(self):
        """Calculate tenure in months"""
        if self.hire_date:
            delta = timezone.now().date() - self.hire_date
            return delta.days // 30
        return 0
    
    @property
    def performance_tier(self):
        """Categorize performance into tiers"""
        score = self.overall_performance_score
        if score >= 90:
            return 'excellent'
        elif score >= 80:
            return 'very_good'
        elif score >= 70:
            return 'good'
        elif score >= 60:
            return 'satisfactory'
        else:
            return 'needs_improvement'

class PerformanceMetric(TimeStampedModel):
    """Individual performance metrics for comprehensive tracking"""
    
    METRIC_CATEGORIES = [
        ('productivity', 'Productivity'),
        ('quality', 'Quality of Work'),
        ('efficiency', 'Efficiency'),
        ('farmer_engagement', 'Farmer Engagement'),
        ('grant_management', 'Grant Management'),
        ('reporting', 'Reporting & Documentation'),
        ('teamwork', 'Teamwork & Collaboration'),
        ('innovation', 'Innovation & Initiative'),
    ]
    
    METRIC_UNITS = [
        ('percentage', 'Percentage (%)'),
        ('count', 'Count'),
        ('currency', 'Currency'),
        ('rating', 'Rating (1-5)'),
        ('hours', 'Hours'),
        ('days', 'Days'),
    ]
    
    staff = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name='performance_metrics',
        verbose_name='Staff Member'
    )
    metric_name = models.CharField(
        max_length=100,
        verbose_name='Metric Name',
        help_text='Name of the performance metric being tracked'
    )
    metric_category = models.CharField(
        max_length=50,
        choices=METRIC_CATEGORIES,
        verbose_name='Metric Category'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Detailed description of what this metric measures'
    )
    
    # Metric Values
    target_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Target Value',
        help_text='Expected target value for this metric'
    )
    actual_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Actual Value',
        help_text='Actual achieved value'
    )
    unit = models.CharField(
        max_length=20,
        choices=METRIC_UNITS,
        verbose_name='Unit of Measurement'
    )
    
    # Time Period
    period_start = models.DateField(
        verbose_name='Period Start',
        help_text='Start date of measurement period'
    )
    period_end = models.DateField(
        verbose_name='Period End',
        help_text='End date of measurement period'
    )
    
    # Performance Calculation
    achievement_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Achievement Rate (%)',
        help_text='Percentage of target achieved'
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Weight (%)',
        help_text='Importance weight in overall performance calculation'
    )
    
    class Meta:
        db_table = 'staff_performance_metric'
        verbose_name = 'Performance Metric'
        verbose_name_plural = 'Performance Metrics'
        ordering = ['staff', '-period_end', 'metric_category']
        indexes = [
            models.Index(fields=['staff', 'period_end']),
            models.Index(fields=['metric_category']),
            models.Index(fields=['achievement_rate']),
        ]
        unique_together = ['staff', 'metric_name', 'period_end']
    
    def save(self, *args, **kwargs):
        """Calculate achievement rate automatically"""
        if self.target_value and self.actual_value and self.target_value > 0:
            self.achievement_rate = (self.actual_value / self.target_value) * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.metric_name} ({self.period_end})"

class KeyPerformanceIndicator(TimeStampedModel):
    """Strategic KPIs for organizational performance tracking"""
    
    KPI_TYPES = [
        ('strategic', 'Strategic KPI'),
        ('operational', 'Operational KPI'),
        ('tactical', 'Tactical KPI'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='KPI Name',
        help_text='Name of the Key Performance Indicator'
    )
    kpi_type = models.CharField(
        max_length=20,
        choices=KPI_TYPES,
        verbose_name='KPI Type'
    )
    description = models.TextField(
        verbose_name='Description',
        help_text='Detailed description and measurement methodology'
    )
    department = models.CharField(
        max_length=50,
        choices=StaffMember.DEPARTMENT_CHOICES,
        verbose_name='Responsible Department'
    )
    
    # Measurement Details
    target_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Target Value'
    )
    current_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Current Value'
    )
    unit = models.CharField(
        max_length=20,
        choices=PerformanceMetric.METRIC_UNITS,
        verbose_name='Unit of Measurement'
    )
    
    # Timeframe
    reporting_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('annually', 'Annually'),
        ],
        verbose_name='Reporting Frequency'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active KPI'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated'
    )
    
    class Meta:
        db_table = 'staff_performance_kpi'
        verbose_name = 'Key Performance Indicator'
        verbose_name_plural = 'Key Performance Indicators'
        ordering = ['department', 'kpi_type', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.department}"
    
    @property
    def achievement_percentage(self):
        """Calculate KPI achievement percentage"""
        if self.target_value and self.current_value and self.target_value > 0:
            return (self.current_value / self.target_value) * 100
        return 0
    
    @property
    def status(self):
        """Determine KPI status based on achievement"""
        achievement = self.achievement_percentage
        if achievement >= 95:
            return 'exceeded'
        elif achievement >= 85:
            return 'achieved'
        elif achievement >= 70:
            return 'moderate'
        else:
            return 'needs_attention'

class PerformanceReview(TimeStampedModel, UUIDModel):
    """Comprehensive performance review system"""
    
    REVIEW_TYPES = [
        ('probation', 'Probation Review'),
        ('quarterly', 'Quarterly Review'),
        ('mid_year', 'Mid-Year Review'),
        ('annual', 'Annual Review'),
        ('promotion', 'Promotion Review'),
        ('special', 'Special Review'),
    ]
    
    RATING_SCALE = [
        (1, '1 - Unsatisfactory'),
        (2, '2 - Needs Improvement'),
        (3, '3 - Meets Expectations'),
        (4, '4 - Exceeds Expectations'),
        (5, '5 - Outstanding'),
    ]
    
    staff = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name='performance_reviews',
        verbose_name='Staff Member'
    )
    review_type = models.CharField(
        max_length=20,
        choices=REVIEW_TYPES,
        verbose_name='Review Type'
    )
    review_period_start = models.DateField(
        verbose_name='Review Period Start'
    )
    review_period_end = models.DateField(
        verbose_name='Review Period End'
    )
    review_date = models.DateField(
        default=timezone.now,
        verbose_name='Review Date'
    )
    
    # Review Participants
    reviewer = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name='conducted_reviews',
        verbose_name='Reviewer',
        help_text='Staff member conducting the review'
    )
    
    # Performance Ratings
    work_quality_rating = models.IntegerField(
        choices=RATING_SCALE,
        verbose_name='Work Quality Rating'
    )
    productivity_rating = models.IntegerField(
        choices=RATING_SCALE,
        verbose_name='Productivity Rating'
    )
    communication_rating = models.IntegerField(
        choices=RATING_SCALE,
        verbose_name='Communication Rating'
    )
    teamwork_rating = models.IntegerField(
        choices=RATING_SCALE,
        verbose_name='Teamwork Rating'
    )
    initiative_rating = models.IntegerField(
        choices=RATING_SCALE,
        verbose_name='Initiative Rating'
    )
    
    # Overall Assessment
    overall_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name='Overall Rating',
        help_text='Average of all rating categories'
    )
    strengths = models.TextField(
        verbose_name='Key Strengths',
        help_text='Areas where staff excels'
    )
    development_areas = models.TextField(
        verbose_name='Development Areas',
        help_text='Areas needing improvement'
    )
    goals_next_period = models.TextField(
        verbose_name='Goals for Next Period',
        help_text='Specific, measurable goals for next review period'
    )
    
    # Review Outcomes
    recommendations = models.TextField(
        blank=True,
        verbose_name='Recommendations',
        help_text='Specific recommendations for development'
    )
    follow_up_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Follow-up Date'
    )
    
    # Status
    is_completed = models.BooleanField(
        default=False,
        verbose_name='Review Completed'
    )
    staff_comments = models.TextField(
        blank=True,
        verbose_name='Staff Comments',
        help_text='Staff member feedback on the review'
    )
    
    class Meta:
        db_table = 'staff_performance_review'
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'
        ordering = ['-review_date', 'staff']
        indexes = [
            models.Index(fields=['staff', 'review_date']),
            models.Index(fields=['review_type', 'is_completed']),
        ]
    
    def save(self, *args, **kwargs):
        """Calculate overall rating automatically"""
        ratings = [
            self.work_quality_rating,
            self.productivity_rating,
            self.communication_rating,
            self.teamwork_rating,
            self.initiative_rating
        ]
        self.overall_rating = sum(ratings) / len(ratings)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.review_type} - {self.review_date}"

class StaffAchievement(TimeStampedModel):
    """Track staff achievements and recognitions"""
    
    ACHIEVEMENT_TYPES = [
        ('award', 'Award'),
        ('certification', 'Certification'),
        ('completion', 'Training Completion'),
        ('innovation', 'Innovation'),
        ('excellence', 'Excellence Recognition'),
        ('milestone', 'Milestone Achievement'),
    ]
    
    staff = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name='Staff Member'
    )
    achievement_type = models.CharField(
        max_length=20,
        choices=ACHIEVEMENT_TYPES,
        verbose_name='Achievement Type'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Achievement Title'
    )
    description = models.TextField(
        verbose_name='Description',
        help_text='Detailed description of the achievement'
    )
    date_achieved = models.DateField(
        verbose_name='Date Achieved'
    )
    
    # Recognition Details
    recognizing_organization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Recognizing Organization'
    )
    certificate_url = models.URLField(
        blank=True,
        verbose_name='Certificate URL',
        help_text='Link to digital certificate or document'
    )
    
    # Impact
    impact_description = models.TextField(
        blank=True,
        verbose_name='Impact Description',
        help_text='How this achievement benefited the organization'
    )
    
    class Meta:
        db_table = 'staff_performance_achievement'
        verbose_name = 'Staff Achievement'
        verbose_name_plural = 'Staff Achievements'
        ordering = ['-date_achieved', 'staff']
        indexes = [
            models.Index(fields=['staff', 'achievement_type']),
        ]
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.title}"

class TrainingDevelopment(TimeStampedModel):
    """Staff training and professional development tracking"""
    
    TRAINING_TYPES = [
        ('technical', 'Technical Skills'),
        ('soft_skills', 'Soft Skills'),
        ('management', 'Management & Leadership'),
        ('compliance', 'Compliance & Regulations'),
        ('technology', 'Technology & Systems'),
        ('sector_specific', 'Sector Specific'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    staff = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name='trainings',
        verbose_name='Staff Member'
    )
    training_title = models.CharField(
        max_length=200,
        verbose_name='Training Title'
    )
    training_type = models.CharField(
        max_length=20,
        choices=TRAINING_TYPES,
        verbose_name='Training Type'
    )
    provider = models.CharField(
        max_length=200,
        verbose_name='Training Provider'
    )
    
    # Training Details
    start_date = models.DateField(
        verbose_name='Start Date'
    )
    end_date = models.DateField(
        verbose_name='End Date'
    )
    duration_hours = models.IntegerField(
        verbose_name='Duration (Hours)',
        help_text='Total training hours'
    )
    
    # Status & Outcomes
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name='Training Status'
    )
    completion_certificate = models.URLField(
        blank=True,
        verbose_name='Completion Certificate URL'
    )
    skills_acquired = models.TextField(
        blank=True,
        verbose_name='Skills Acquired',
        help_text='Key skills and knowledge gained'
    )
    
    # Evaluation
    training_rating = models.IntegerField(
        choices=PerformanceReview.RATING_SCALE,
        null=True,
        blank=True,
        verbose_name='Training Rating',
        help_text='Staff rating of training quality'
    )
    application_plan = models.TextField(
        blank=True,
        verbose_name='Application Plan',
        help_text='How skills will be applied in work'
    )
    
    class Meta:
        db_table = 'staff_performance_training'
        verbose_name = 'Training & Development'
        verbose_name_plural = 'Trainings & Development'
        ordering = ['-start_date', 'staff']
        indexes = [
            models.Index(fields=['staff', 'status']),
            models.Index(fields=['training_type']),
        ]
    
    def __str__(self):
        return f"{self.staff.full_name} - {self.training_title}"
    
    @property
    def is_upcoming(self):
        """Check if training is upcoming"""
        return self.status == 'planned' and self.start_date > timezone.now().date()
    
    @property
    def is_ongoing(self):
        """Check if training is currently ongoing"""
        today = timezone.now().date()
        return (self.status == 'in_progress' and 
                self.start_date <= today <= self.end_date)
