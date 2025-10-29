from django.contrib import admin
from django.utils.html import format_html
from .models import (
    VideoCallSession, 
    CallParticipant, 
    CallRecording, 
    ChatMessage, 
    VideoCallSettings
)

@admin.register(VideoCallSession)
class VideoCallSessionAdmin(admin.ModelAdmin):
    """Professional admin interface for Video Call Session management"""
    
    list_display = [
        'title', 
        'session_id',
        'call_type_display',
        'host',
        'scheduled_time_display',
        'status_display',
        'participant_count_display',
        'duration_display'
    ]
    
    list_filter = [
        'call_type', 
        'status',
        'scheduled_time',
        'host__department'
    ]
    
    search_fields = [
        'title', 
        'session_id',
        'host__user__first_name',
        'host__user__last_name',
        'description'
    ]
    
    readonly_fields = [
        'session_id',
        'participant_count_display',
        'duration_display',
        'join_url_display',
        'is_active_display',
        'is_upcoming_display'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'session_id',
                'call_type',
                'description'
            )
        }),
        ('Scheduling', {
            'fields': (
                'scheduled_time',
                'actual_start_time',
                'actual_end_time',
                'duration_display'
            )
        }),
        ('Host & Participants', {
            'fields': (
                'host',
                'co_hosts',
                'max_participants',
                'participant_count_display'
            )
        }),
        ('Access Control', {
            'fields': (
                'is_public',
                'meeting_password',
                'join_url_display'
            )
        }),
        ('Status & Technical', {
            'fields': (
                'status',
                'room_url',
                'is_active_display',
                'is_upcoming_display'
            )
        }),
        ('Recording & Integration', {
            'fields': (
                'is_recorded',
                'recording_url',
                'related_meeting',
                'related_training'
            )
        })
    )
    
    filter_horizontal = ['co_hosts']
    
    def call_type_display(self, obj):
        type_colors = {
            'staff_meeting': 'blue',
            'farmer_training': 'green',
            'cbo_meeting': 'purple',
            'one_on_one': 'orange',
            'emergency': 'red',
            'training': 'teal'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            type_colors.get(obj.call_type, 'black'),
            obj.get_call_type_display()
        )
    call_type_display.short_description = 'Call Type'
    
    def scheduled_time_display(self, obj):
        return obj.scheduled_time.strftime("%b %d, %Y %I:%M %p")
    scheduled_time_display.short_description = 'Scheduled Time'
    scheduled_time_display.admin_order_field = 'scheduled_time'
    
    def status_display(self, obj):
        status_colors = {
            'scheduled': 'blue',
            'active': 'green',
            'completed': 'gray',
            'cancelled': 'red',
            'failed': 'darkred'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            status_colors.get(obj.status, 'black'),
            obj.status
        )
    status_display.short_description = 'Status'
    
    def participant_count_display(self, obj):
        color = 'green' if obj.participant_count > 0 else 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/{} participants</span>',
            color,
            obj.participant_count,
            obj.max_participants
        )
    participant_count_display.short_description = 'Participants'
    
    def duration_display(self, obj):
        if obj.duration_minutes > 0:
            return f"{obj.duration_minutes:.1f} minutes"
        return "Not completed"
    duration_display.short_description = 'Duration'
    
    def join_url_display(self, obj):
        return format_html(
            '<a href="{}" target="_blank" style="color: blue; text-decoration: underline;">Join Meeting</a>',
            obj.join_url
        )
    join_url_display.short_description = 'Join URL'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;"> Active</span>')
        return format_html('<span style="color: gray;"> Not active</span>')
    is_active_display.short_description = 'Active Status'
    
    def is_upcoming_display(self, obj):
        if obj.is_upcoming:
            return format_html('<span style="color: orange;"> Upcoming</span>')
        return format_html('<span style="color: gray;"> Not upcoming</span>')
    is_upcoming_display.short_description = 'Upcoming Status'

@admin.register(CallParticipant)
class CallParticipantAdmin(admin.ModelAdmin):
    """Admin interface for detailed call participant tracking"""
    
    list_display = [
        'staff_member',
        'session_display',
        'role_display',
        'join_time_display',
        'left_at_display',
        'duration_display',
        'is_active_display',
        'connection_quality_display'
    ]
    
    list_filter = [
        'role',
        'session__call_type',
        'join_time'
    ]
    
    search_fields = [
        'staff_member__user__first_name',
        'staff_member__user__last_name',
        'session__title'
    ]
    
    readonly_fields = ['duration_display', 'is_active_display']
    
    def session_display(self, obj):
        return obj.session.title
    session_display.short_description = 'Session'
    session_display.admin_order_field = 'session__title'
    
    def role_display(self, obj):
        role_colors = {
            'host': 'red',
            'co_host': 'orange',
            'presenter': 'purple',
            'participant': 'blue',
            'viewer': 'gray'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            role_colors.get(obj.role, 'black'),
            obj.role.replace('_', ' ')
        )
    role_display.short_description = 'Role'
    
    def join_time_display(self, obj):
        if obj.join_time:
            return obj.join_time.strftime("%b %d, %Y %I:%M %p")
        return "Not joined"
    join_time_display.short_description = 'Join Time'
    
    def left_at_display(self, obj):
        if obj.left_at:
            return obj.left_at.strftime("%b %d, %Y %I:%M %p")
        return "Still in call"
    left_at_display.short_description = 'Left At'
    
    def duration_display(self, obj):
        if obj.duration_minutes > 0:
            return f"{obj.duration_minutes:.1f} minutes"
        return "Active"
    duration_display.short_description = 'Duration'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;"> In call</span>')
        return format_html('<span style="color: gray;"> Left call</span>')
    is_active_display.short_description = 'Active'
    
    def connection_quality_display(self, obj):
        if obj.connection_quality:
            color = 'green' if obj.connection_quality >= 4.0 else \
                    'orange' if obj.connection_quality >= 3.0 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}/5</span>',
                color,
                obj.connection_quality
            )
        return "Not measured"
    connection_quality_display.short_description = 'Connection'

@admin.register(CallRecording)
class CallRecordingAdmin(admin.ModelAdmin):
    """Admin interface for call recording management"""
    
    list_display = [
        'session',
        'start_time_display',
        'duration_display',
        'file_size_display',
        'status_display',
        'download_count'
    ]
    
    list_filter = [
        'status',
        'start_time',
        'is_public'
    ]
    
    def start_time_display(self, obj):
        return obj.start_time.strftime("%b %d, %Y %I:%M %p")
    start_time_display.short_description = 'Start Time'
    
    def duration_display(self, obj):
        return f"{obj.duration_minutes:.1f} minutes"
    duration_display.short_description = 'Duration'
    
    def file_size_display(self, obj):
        return f"{obj.file_size_mb:.1f} MB"
    file_size_display.short_description = 'File Size'
    
    def status_display(self, obj):
        status_colors = {
            'processing': 'blue',
            'completed': 'green',
            'failed': 'red',
            'deleted': 'gray'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            status_colors.get(obj.status, 'black'),
            obj.status
        )
    status_display.short_description = 'Status'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Admin interface for chat messages"""
    
    list_display = [
        'sender',
        'session',
        'message_type_display',
        'content_preview',
        'created_at_display',
        'is_pinned_display'
    ]
    
    list_filter = [
        'message_type',
        'is_pinned',
        'created_at'
    ]
    
    def message_type_display(self, obj):
        type_colors = {
            'text': 'blue',
            'file': 'green',
            'system': 'gray',
            'announcement': 'orange'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            type_colors.get(obj.message_type, 'black'),
            obj.get_message_type_display()
        )
    message_type_display.short_description = 'Type'
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime("%b %d, %Y %I:%M %p")
    created_at_display.short_description = 'Sent At'
    
    def is_pinned_display(self, obj):
        if obj.is_pinned:
            return format_html('<span style="color: orange;"> Pinned</span>')
        return ""
    is_pinned_display.short_description = 'Pinned'

@admin.register(VideoCallSettings)
class VideoCallSettingsAdmin(admin.ModelAdmin):
    """Admin interface for organization-wide video call settings"""
    
    list_display = [
        'organization_name',
        'enable_recording_display',
        'enable_screen_share_display',
        'require_password_display',
        'max_participants_default'
    ]
    
    def enable_recording_display(self, obj):
        if obj.enable_recording:
            return format_html('<span style="color: green;"> Enabled</span>')
        return format_html('<span style="color: red;"> Disabled</span>')
    enable_recording_display.short_description = 'Recording'
    
    def enable_screen_share_display(self, obj):
        if obj.enable_screen_share:
            return format_html('<span style="color: green;"> Enabled</span>')
        return format_html('<span style="color: red;"> Disabled</span>')
    enable_screen_share_display.short_description = 'Screen Share'
    
    def require_password_display(self, obj):
        if obj.require_password:
            return format_html('<span style="color: green;"> Required</span>')
        return format_html('<span style="color: orange;"> Optional</span>')
    require_password_display.short_description = 'Password'
