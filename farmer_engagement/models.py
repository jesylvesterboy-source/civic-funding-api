# farmer_engagement/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import qrcode
from io import BytesIO
from django.core.files import File
import uuid

class TimeStampedModel(models.Model):
    """Abstract base model with created and modified timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class CBOGroup(TimeStampedModel):
    """Community-Based Organization Groups with comprehensive tracking"""
    
    GROUP_TYPES = [
        ('farmer_cooperative', 'Farmer Cooperative'),
        ('producer_group', 'Producer Group'),
        ('savings_group', 'Savings & Credit Group'),
        ('marketing_group', 'Marketing Group'),
        ('processing_group', 'Processing Group'),
        ('women_group', "Women's Group"),
        ('youth_group', 'Youth Group'),
    ]
    
    GROUP_STATUS = [
        ('forming', 'Forming'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('dormant', 'Dormant'),
        ('dissolved', 'Dissolved'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200,
        verbose_name='CBO Name',
        help_text='Official name of the community-based organization'
    )
    group_type = models.CharField(
        max_length=50,
        choices=GROUP_TYPES,
        verbose_name='Group Type'
    )
    registration_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Registration Number',
        help_text='Official registration number if registered'
    )
    
    # Location Information
    village = models.CharField(max_length=100, verbose_name='Village')
    parish = models.CharField(max_length=100, verbose_name='Parish')
    sub_county = models.CharField(max_length=100, verbose_name='Sub-County')
    district = models.CharField(max_length=100, verbose_name='District')
    gps_latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='GPS Latitude'
    )
    gps_longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='GPS Longitude'
    )
    
    # Group Details
    formation_date = models.DateField(
        verbose_name='Formation Date',
        help_text='Date when the group was officially formed'
    )
    status = models.CharField(
        max_length=20,
        choices=GROUP_STATUS,
        default='active',
        verbose_name='Group Status'
    )
    total_members = models.IntegerField(
        default=0,
        verbose_name='Total Members',
        help_text='Current number of registered members'
    )
    female_members = models.IntegerField(
        default=0,
        verbose_name='Female Members',
        help_text='Number of female members'
    )
    male_members = models.IntegerField(
        default=0,
        verbose_name='Male Members',
        help_text='Number of male members'
    )
    
    # Leadership
    chairperson_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Chairperson Name'
    )
    chairperson_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Chairperson Phone'
    )
    secretary_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Secretary Name'
    )
    treasurer_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Treasurer Name'
    )
    
    # Staff Assignment
    assigned_staff = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_cbo_groups',
        verbose_name='Assigned Staff',
        help_text='Staff member responsible for this CBO'
    )
    
    class Meta:
        db_table = 'farmer_engagement_cbogroup'
        verbose_name = 'CBO Group'
        verbose_name_plural = 'CBO Groups'
        ordering = ['name', 'district']
        indexes = [
            models.Index(fields=['group_type', 'status']),
            models.Index(fields=['district', 'sub_county']),
            models.Index(fields=['assigned_staff']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.district}"
    
    @property
    def location(self):
        return f"{self.village}, {self.parish}, {self.sub_county}"
    
    @property
    def gender_balance(self):
        if self.total_members > 0:
            return (self.female_members / self.total_members) * 100
        return 0
    
    def clean(self):
        if self.total_members < (self.female_members + self.male_members):
            raise ValidationError('Total members cannot be less than the sum of female and male members.')

class CBOMeeting(TimeStampedModel):
    """CBO Meeting management with QR code attendance tracking"""
    
    MEETING_TYPES = [
        ('regular', 'Regular Meeting'),
        ('special', 'Special Meeting'),
        ('training', 'Training Session'),
        ('planning', 'Planning Meeting'),
        ('election', 'Election Meeting'),
        ('emergency', 'Emergency Meeting'),
    ]
    
    MEETING_STATUS = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cbo_group = models.ForeignKey(
        CBOGroup,
        on_delete=models.CASCADE,
        related_name='meetings',
        verbose_name='CBO Group'
    )
    meeting_type = models.CharField(
        max_length=20,
        choices=MEETING_TYPES,
        default='regular',
        verbose_name='Meeting Type'
    )
    
    # Meeting Details
    title = models.CharField(
        max_length=200,
        verbose_name='Meeting Title',
        help_text='Descriptive title for the meeting'
    )
    agenda = models.TextField(
        verbose_name='Meeting Agenda',
        help_text='Detailed agenda items to be discussed'
    )
    objectives = models.TextField(
        blank=True,
        verbose_name='Meeting Objectives',
        help_text='Specific objectives for this meeting'
    )
    
    # Time and Location
    meeting_date = models.DateTimeField(
        verbose_name='Meeting Date & Time'
    )
    venue = models.CharField(
        max_length=200,
        verbose_name='Meeting Venue',
        help_text='Physical location of the meeting'
    )
    gps_latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='Venue GPS Latitude'
    )
    gps_longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='Venue GPS Longitude'
    )
    
    # Facilitation
    facilitator = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.CASCADE,
        related_name='facilitated_meetings',
        verbose_name='Facilitator',
        help_text='Staff member facilitating the meeting'
    )
    co_facilitator = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='co_facilitated_meetings',
        verbose_name='Co-Facilitator'
    )
    
    # Status and Tracking
    status = models.CharField(
        max_length=20,
        choices=MEETING_STATUS,
        default='scheduled',
        verbose_name='Meeting Status'
    )
    expected_attendance = models.IntegerField(
        default=0,
        verbose_name='Expected Attendance',
        help_text='Number of members expected to attend'
    )
    actual_attendance = models.IntegerField(
        default=0,
        verbose_name='Actual Attendance',
        help_text='Number of members who actually attended'
    )
    
    # QR Code for Attendance
    qr_code = models.ImageField(
        upload_to='meeting_qrcodes/',
        blank=True,
        null=True,
        verbose_name='QR Code',
        help_text='QR code for digital attendance tracking'
    )
    
    # Meeting Outcomes
    minutes = models.TextField(
        blank=True,
        verbose_name='Meeting Minutes',
        help_text='Detailed minutes and resolutions'
    )
    action_points = models.TextField(
        blank=True,
        verbose_name='Action Points',
        help_text='Specific actions agreed upon with responsibilities'
    )
    next_meeting_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Next Meeting Date'
    )
    
    class Meta:
        db_table = 'farmer_engagement_cbomeeting'
        verbose_name = 'CBO Meeting'
        verbose_name_plural = 'CBO Meetings'
        ordering = ['-meeting_date', 'cbo_group']
        indexes = [
            models.Index(fields=['cbo_group', 'meeting_date']),
            models.Index(fields=['meeting_type', 'status']),
            models.Index(fields=['facilitator', 'meeting_date']),
        ]
    
    def __str__(self):
        return f"{self.cbo_group.name} - {self.title} - {self.meeting_date.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        # Generate QR code if not exists
        if not self.qr_code and self.pk:
            self.generate_qr_code()
        super().save(*args, **kwargs)
    
    def generate_qr_code(self):
        """Generate QR code for meeting attendance"""
        qr_data = f"{settings.SITE_URL}/meetings/{self.id}/checkin/"
        qr_image = qrcode.make(qr_data)
        
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        
        filename = f'meeting_qr_{self.id}.png'
        self.qr_code.save(filename, File(buffer), save=False)
    
    @property
    def attendance_rate(self):
        if self.expected_attendance > 0:
            return (self.actual_attendance / self.expected_attendance) * 100
        return 0
    
    @property
    def is_upcoming(self):
        return self.status == 'scheduled' and self.meeting_date > timezone.now()
    
    @property
    def is_ongoing(self):
        return self.status == 'ongoing'

class FarmerAttendance(TimeStampedModel):
    """Detailed farmer attendance tracking with digital check-in"""
    
    ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    
    CHECKIN_METHODS = [
        ('qr_code', 'QR Code Scan'),
        ('manual', 'Manual Entry'),
        ('biometric', 'Biometric'),
        ('nfc', 'NFC Tag'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(
        'farmers.Farmer',
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='Farmer'
    )
    meeting = models.ForeignKey(
        CBOMeeting,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='CBO Meeting'
    )
    
    # Attendance Details
    attendance_status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUS,
        default='present',
        verbose_name='Attendance Status'
    )
    check_in_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Check-in Time',
        help_text='Actual time when farmer checked in'
    )
    check_out_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Check-out Time',
        help_text='Time when farmer checked out (if applicable)'
    )
    checkin_method = models.CharField(
        max_length=20,
        choices=CHECKIN_METHODS,
        default='manual',
        verbose_name='Check-in Method'
    )
    
    # Verification
    verified_by = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Verified By',
        help_text='Staff member who verified the attendance'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Attendance Notes',
        help_text='Any additional notes about attendance'
    )
    
    class Meta:
        db_table = 'farmer_engagement_attendance'
        verbose_name = 'Farmer Attendance'
        verbose_name_plural = 'Farmer Attendances'
        ordering = ['-check_in_time', 'farmer']
        indexes = [
            models.Index(fields=['farmer', 'meeting']),
            models.Index(fields=['meeting', 'attendance_status']),
            models.Index(fields=['check_in_time']),
        ]
        unique_together = ['farmer', 'meeting']
    
    def __str__(self):
        return f"{self.farmer.full_name} - {self.meeting.title}"
    
    @property
    def duration_minutes(self):
        if self.check_in_time and self.check_out_time:
            duration = self.check_out_time - self.check_in_time
            return duration.total_seconds() / 60
        return 0
    
    @property
    def was_late(self):
        if self.check_in_time and self.meeting.meeting_date:
            # Consider late if more than 15 minutes after meeting start
            late_threshold = 15
            time_difference = (self.check_in_time - self.meeting.meeting_date).total_seconds() / 60
            return time_difference > late_threshold
        return False

class MeetingDocument(TimeStampedModel):
    """Supporting documents for CBO meetings"""
    
    DOCUMENT_TYPES = [
        ('attendance_list', 'Attendance List'),
        ('minutes', 'Meeting Minutes'),
        ('presentation', 'Presentation Slides'),
        ('photo', 'Meeting Photo'),
        ('resolution', 'Resolution Document'),
        ('other', 'Other Document'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meeting = models.ForeignKey(
        CBOMeeting,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='CBO Meeting'
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        verbose_name='Document Type'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Document Title'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    file = models.FileField(
        upload_to='meeting_documents/%Y/%m/%d/',
        verbose_name='Document File'
    )
    uploaded_by = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.CASCADE,
        verbose_name='Uploaded By'
    )
    
    class Meta:
        db_table = 'farmer_engagement_document'
        verbose_name = 'Meeting Document'
        verbose_name_plural = 'Meeting Documents'
        ordering = ['-created_at', 'meeting']
    
    def __str__(self):
        return f"{self.meeting.title} - {self.title}"

class CBOTraining(TimeStampedModel):
    """Specialized training sessions for CBO groups"""
    
    TRAINING_CATEGORIES = [
        ('agricultural', 'Agricultural Practices'),
        ('financial', 'Financial Literacy'),
        ('leadership', 'Leadership & Governance'),
        ('marketing', 'Marketing & Value Addition'),
        ('climate', 'Climate Smart Agriculture'),
        ('technology', 'Technology Adoption'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cbo_group = models.ForeignKey(
        CBOGroup,
        on_delete=models.CASCADE,
        related_name='trainings',
        verbose_name='CBO Group'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Training Title'
    )
    training_category = models.CharField(
        max_length=50,
        choices=TRAINING_CATEGORIES,
        verbose_name='Training Category'
    )
    description = models.TextField(
        verbose_name='Training Description'
    )
    objectives = models.TextField(
        verbose_name='Training Objectives'
    )
    
    # Training Details
    start_date = models.DateTimeField(
        verbose_name='Start Date & Time'
    )
    end_date = models.DateTimeField(
        verbose_name='End Date & Time'
    )
    venue = models.CharField(
        max_length=200,
        verbose_name='Training Venue'
    )
    
    # Facilitation
    facilitator = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.CASCADE,
        related_name='conducted_trainings',
        verbose_name='Facilitator'
    )
    resource_persons = models.ManyToManyField(
        'staff_performance.StaffMember',
        related_name='assisted_trainings',
        blank=True,
        verbose_name='Resource Persons'
    )
    
    # Attendance and Evaluation
    total_participants = models.IntegerField(
        default=0,
        verbose_name='Total Participants'
    )
    training_materials = models.TextField(
        blank=True,
        verbose_name='Training Materials Used'
    )
    evaluation_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Evaluation Score',
        help_text='Average evaluation score from participants (1-5)'
    )
    
    class Meta:
        db_table = 'farmer_engagement_training'
        verbose_name = 'CBO Training'
        verbose_name_plural = 'CBO Trainings'
        ordering = ['-start_date', 'cbo_group']
    
    def __str__(self):
        return f"{self.cbo_group.name} - {self.title}"
    
    @property
    def duration_hours(self):
        if self.start_date and self.end_date:
            duration = self.end_date - self.start_date
            return duration.total_seconds() / 3600
        return 0
