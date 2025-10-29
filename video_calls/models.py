# video_calls/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import secrets

class TimeStampedModel(models.Model):
    """Abstract base model with created and modified timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class VideoCallSession(TimeStampedModel):
    """Video call session management with WebRTC integration"""
    
    CALL_TYPES = [
        ('staff_meeting', 'Staff Meeting'),
        ('farmer_training', 'Farmer Training'),
        ('cbo_meeting', 'CBO Virtual Meeting'),
        ('one_on_one', 'One-on-One Consultation'),
        ('emergency', 'Emergency Meeting'),
        ('training', 'Training Session'),
    ]
    
    CALL_STATUS = [
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Session ID',
        help_text='Unique identifier for the video call session'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Call Title',
        help_text='Descriptive title for the video call'
    )
    call_type = models.CharField(
        max_length=50,
        choices=CALL_TYPES,
        verbose_name='Call Type'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Purpose and agenda for the video call'
    )
    
    # Scheduling
    scheduled_time = models.DateTimeField(
        verbose_name='Scheduled Time',
        help_text='Planned start time for the video call'
    )
    actual_start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Actual Start Time'
    )
    actual_end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Actual End Time'
    )
    
    # Host and Participants
    host = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.CASCADE,
        related_name='hosted_video_calls',
        verbose_name='Call Host',
        help_text='Staff member hosting the video call'
    )
    co_hosts = models.ManyToManyField(
        'staff_performance.StaffMember',
        related_name='co_hosted_video_calls',
        blank=True,
        verbose_name='Co-hosts',
        help_text='Additional staff members with host privileges'
    )
    
    # Access Control
    meeting_password = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Meeting Password',
        help_text='Optional password for meeting access'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Public Meeting',
        help_text='Allow anyone with link to join (without staff authentication)'
    )
    max_participants = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        verbose_name='Maximum Participants',
        help_text='Maximum number of participants allowed'
    )
    
    # Status and Tracking
    status = models.CharField(
        max_length=20,
        choices=CALL_STATUS,
        default='scheduled',
        verbose_name='Call Status'
    )
    room_url = models.URLField(
        blank=True,
        verbose_name='Room URL',
        help_text='WebRTC room URL for participants to join'
    )
    
    # Recording and Analytics
    is_recorded = models.BooleanField(
        default=False,
        verbose_name='Record Call',
        help_text='Automatically record the video call session'
    )
    recording_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Recording URL',
        help_text='URL to access the recorded session'
    )
    duration_minutes = models.IntegerField(
        default=0,
        verbose_name='Duration (Minutes)',
        help_text='Actual duration of the call in minutes'
    )
    
    # Integration with other modules
    related_meeting = models.ForeignKey(
        'farmer_engagement.CBOMeeting',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='video_calls',
        verbose_name='Related CBO Meeting',
        help_text='Link this video call to a physical CBO meeting'
    )
    related_training = models.ForeignKey(
        'farmer_engagement.CBOTraining',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='video_calls',
        verbose_name='Related Training',
        help_text='Link this video call to a training session'
    )
    
    class Meta:
        db_table = 'video_calls_session'
        verbose_name = 'Video Call Session'
        verbose_name_plural = 'Video Call Sessions'
        ordering = ['-scheduled_time', 'title']
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['host', 'scheduled_time']),
            models.Index(fields=['call_type', 'status']),
            models.Index(fields=['scheduled_time', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.session_id}"
    
    def save(self, *args, **kwargs):
        if not self.session_id:
            # Generate unique session ID
            self.session_id = f"vc_{secrets.token_urlsafe(12)}"
        
        if not self.meeting_password and not self.is_public:
            # Generate secure password if not public
            self.meeting_password = secrets.token_urlsafe(8)
            
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def is_upcoming(self):
        return self.status == 'scheduled' and self.scheduled_time > timezone.now()
    
    @property
    def participant_count(self):
        return self.participants.filter(left_at__isnull=True).count()
    
    @property
    def join_url(self):
        return f"{settings.SITE_URL}/video/join/{self.session_id}/"

class CallParticipant(TimeStampedModel):
    """Detailed participant tracking for video calls"""
    
    PARTICIPANT_ROLES = [
        ('host', 'Host'),
        ('co_host', 'Co-host'),
        ('presenter', 'Presenter'),
        ('participant', 'Participant'),
        ('viewer', 'Viewer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        VideoCallSession,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name='Video Call Session'
    )
    staff_member = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.CASCADE,
        related_name='video_call_participations',
        verbose_name='Staff Participant'
    )
    
    # Participation Details
    role = models.CharField(
        max_length=20,
        choices=PARTICIPANT_ROLES,
        default='participant',
        verbose_name='Participant Role'
    )
    join_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Join Time',
        help_text='Time when participant joined the call'
    )
    left_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Left At',
        help_text='Time when participant left the call'
    )
    
    # Technical Details
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent',
        help_text='Browser and device information'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP Address'
    )
    connection_quality = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Connection Quality',
        help_text='Average connection quality rating (0-5)'
    )
    
    # Permissions
    has_audio = models.BooleanField(
        default=True,
        verbose_name='Audio Enabled',
        help_text='Participant has audio capabilities'
    )
    has_video = models.BooleanField(
        default=True,
        verbose_name='Video Enabled',
        help_text='Participant has video capabilities'
    )
    can_share_screen = models.BooleanField(
        default=False,
        verbose_name='Can Share Screen',
        help_text='Participant has screen sharing permission'
    )
    can_chat = models.BooleanField(
        default=True,
        verbose_name='Can Chat',
        help_text='Participant can use chat features'
    )
    
    class Meta:
        db_table = 'video_calls_participant'
        verbose_name = 'Call Participant'
        verbose_name_plural = 'Call Participants'
        ordering = ['-join_time', 'staff_member']
        indexes = [
            models.Index(fields=['session', 'staff_member']),
            models.Index(fields=['join_time', 'left_at']),
            models.Index(fields=['role']),
        ]
        unique_together = ['session', 'staff_member']
    
    def __str__(self):
        return f"{self.staff_member.full_name} - {self.session.title}"
    
    @property
    def duration_minutes(self):
        if self.join_time and self.left_at:
            duration = self.left_at - self.join_time
            return duration.total_seconds() / 60
        elif self.join_time and not self.left_at:
            # Still in call
            duration = timezone.now() - self.join_time
            return duration.total_seconds() / 60
        return 0
    
    @property
    def is_active(self):
        return self.join_time is not None and self.left_at is None

class CallRecording(TimeStampedModel):
    """Video call recording management"""
    
    RECORDING_STATUS = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('deleted', 'Deleted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        VideoCallSession,
        on_delete=models.CASCADE,
        related_name='recordings',
        verbose_name='Video Call Session'
    )
    
    # Recording Details
    start_time = models.DateTimeField(
        verbose_name='Recording Start Time'
    )
    end_time = models.DateTimeField(
        verbose_name='Recording End Time'
    )
    file_size = models.BigIntegerField(
        default=0,
        verbose_name='File Size (Bytes)',
        help_text='Size of the recording file in bytes'
    )
    duration_seconds = models.IntegerField(
        default=0,
        verbose_name='Duration (Seconds)'
    )
    
    # Storage and Access
    file_url = models.URLField(
        verbose_name='Recording URL',
        help_text='URL to access the recording file'
    )
    thumbnail_url = models.URLField(
        blank=True,
        verbose_name='Thumbnail URL',
        help_text='URL to recording thumbnail image'
    )
    status = models.CharField(
        max_length=20,
        choices=RECORDING_STATUS,
        default='processing',
        verbose_name='Recording Status'
    )
    
    # Access Control
    is_public = models.BooleanField(
        default=False,
        verbose_name='Public Recording',
        help_text='Make recording publicly accessible'
    )
    download_count = models.IntegerField(
        default=0,
        verbose_name='Download Count',
        help_text='Number of times recording was downloaded'
    )
    
    class Meta:
        db_table = 'video_calls_recording'
        verbose_name = 'Call Recording'
        verbose_name_plural = 'Call Recordings'
        ordering = ['-start_time', 'session']
        indexes = [
            models.Index(fields=['session', 'start_time']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.session.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def duration_minutes(self):
        return self.duration_seconds / 60
    
    @property
    def file_size_mb(self):
        return self.file_size / (1024 * 1024)

class ChatMessage(TimeStampedModel):
    """Real-time chat messages during video calls"""
    
    MESSAGE_TYPES = [
        ('text', 'Text Message'),
        ('file', 'File Attachment'),
        ('system', 'System Message'),
        ('announcement', 'Announcement'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        VideoCallSession,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        verbose_name='Video Call Session'
    )
    sender = models.ForeignKey(
        'staff_performance.StaffMember',
        on_delete=models.CASCADE,
        related_name='sent_chat_messages',
        verbose_name='Message Sender'
    )
    
    # Message Content
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default='text',
        verbose_name='Message Type'
    )
    content = models.TextField(
        verbose_name='Message Content',
        help_text='Text content of the message'
    )
    file_attachment = models.FileField(
        upload_to='chat_attachments/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='File Attachment'
    )
    
    # Metadata
    is_pinned = models.BooleanField(
        default=False,
        verbose_name='Pinned Message',
        help_text='Pin this message to top of chat'
    )
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Reply To Message'
    )
    
    class Meta:
        db_table = 'video_calls_chatmessage'
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender.full_name}: {self.content[:50]}..."

class VideoCallSettings(TimeStampedModel):
    """Organization-wide video call settings and configuration"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization_name = models.CharField(
        max_length=200,
        default='FSSS Organization',
        verbose_name='Organization Name',
        help_text='Name displayed in video call interface'
    )
    
    # WebRTC Configuration
    stun_servers = models.TextField(
        default='stun:stun.l.google.com:19302',
        verbose_name='STUN Servers',
        help_text='STUN server URLs (one per line)'
    )
    turn_servers = models.TextField(
        blank=True,
        verbose_name='TURN Servers',
        help_text='TURN server URLs with credentials (one per line)'
    )
    
    # Feature Flags
    enable_recording = models.BooleanField(
        default=True,
        verbose_name='Enable Recording',
        help_text='Allow call recording functionality'
    )
    enable_screen_share = models.BooleanField(
        default=True,
        verbose_name='Enable Screen Sharing',
        help_text='Allow screen sharing during calls'
    )
    enable_chat = models.BooleanField(
        default=True,
        verbose_name='Enable Chat',
        help_text='Enable real-time chat during calls'
    )
    enable_breakout_rooms = models.BooleanField(
        default=False,
        verbose_name='Enable Breakout Rooms',
        help_text='Allow creating breakout rooms during calls'
    )
    
    # Security Settings
    require_password = models.BooleanField(
        default=True,
        verbose_name='Require Meeting Password',
        help_text='Require password for all meetings by default'
    )
    allow_public_meetings = models.BooleanField(
        default=False,
        verbose_name='Allow Public Meetings',
        help_text='Allow meetings without authentication'
    )
    max_participants_default = models.IntegerField(
        default=50,
        verbose_name='Default Max Participants',
        help_text='Default maximum participants for new meetings'
    )
    
    # Branding
    logo_url = models.URLField(
        blank=True,
        verbose_name='Logo URL',
        help_text='Organization logo displayed in video calls'
    )
    primary_color = models.CharField(
        max_length=7,
        default='#3B82F6',
        verbose_name='Primary Color',
        help_text='Primary brand color (hex code)'
    )
    
    class Meta:
        db_table = 'video_calls_settings'
        verbose_name = 'Video Call Settings'
        verbose_name_plural = 'Video Call Settings'
    
    def __str__(self):
        return f"Video Call Settings - {self.organization_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and VideoCallSettings.objects.exists():
            raise ValidationError('Only one VideoCallSettings instance can exist')
        super().save(*args, **kwargs)
