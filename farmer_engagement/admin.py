from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CBOGroup, 
    CBOMeeting, 
    FarmerAttendance, 
    MeetingDocument, 
    CBOTraining
)

@admin.register(CBOGroup)
class CBOGroupAdmin(admin.ModelAdmin):
    """Professional admin interface for CBO Group management"""
    
    list_display = [
        'name', 
        'group_type', 
        'district', 
        'sub_county',
        'total_members_display',
        'gender_balance_display',
        'status',
        'assigned_staff'
    ]
    
    list_filter = [
        'group_type', 
        'status',
        'district',
        'sub_county',
        'assigned_staff'
    ]
    
    search_fields = [
        'name', 
        'village', 
        'parish',
        'chairperson_name',
        'registration_number'
    ]
    
    readonly_fields = ['gender_balance_display', 'location_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'group_type',
                'registration_number',
                'formation_date',
                'status'
            )
        }),
        ('Location Details', {
            'fields': (
                'village',
                'parish', 
                'sub_county',
                'district',
                'gps_latitude',
                'gps_longitude',
                'location_display'
            )
        }),
        ('Membership Details', {
            'fields': (
                'total_members',
                'female_members',
                'male_members',
                'gender_balance_display'
            )
        }),
        ('Leadership', {
            'fields': (
                'chairperson_name',
                'chairperson_phone', 
                'secretary_name',
                'treasurer_name'
            )
        }),
        ('Staff Assignment', {
            'fields': ('assigned_staff',)
        })
    )
    
    def total_members_display(self, obj):
        return f"{obj.total_members} members"
    total_members_display.short_description = 'Total Members'
    
    def gender_balance_display(self, obj):
        color = 'green' if obj.gender_balance >= 40 else 'orange'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}% female</span>',
            color,
            obj.gender_balance
        )
    gender_balance_display.short_description = 'Gender Balance'
    
    def location_display(self, obj):
        return obj.location
    location_display.short_description = 'Full Location'

@admin.register(CBOMeeting)
class CBOMeetingAdmin(admin.ModelAdmin):
    """Admin interface for CBO Meetings with attendance tracking"""
    
    list_display = [
        'title',
        'cbo_group',
        'meeting_type',
        'meeting_date_display',
        'status_display',
        'attendance_rate_display',
        'facilitator'
    ]
    
    list_filter = [
        'meeting_type',
        'status', 
        'meeting_date',
        'cbo_group__district'
    ]
    
    search_fields = [
        'title',
        'agenda',
        'cbo_group__name',
        'venue'
    ]
    
    readonly_fields = [
        'attendance_rate_display',
        'qr_code_display',
        'is_upcoming_display',
        'is_ongoing_display'
    ]
    
    fieldsets = (
        ('Meeting Information', {
            'fields': (
                'cbo_group',
                'meeting_type', 
                'title',
                'agenda',
                'objectives'
            )
        }),
        ('Time & Location', {
            'fields': (
                'meeting_date',
                'venue',
                'gps_latitude',
                'gps_longitude'
            )
        }),
        ('Facilitation', {
            'fields': (
                'facilitator',
                'co_facilitator'
            )
        }),
        ('Attendance', {
            'fields': (
                'expected_attendance',
                'actual_attendance',
                'attendance_rate_display'
            )
        }),
        ('Status & Tracking', {
            'fields': (
                'status',
                'is_upcoming_display',
                'is_ongoing_display',
                'qr_code_display'
            )
        }),
        ('Outcomes', {
            'fields': (
                'minutes',
                'action_points', 
                'next_meeting_date'
            )
        })
    )
    
    def meeting_date_display(self, obj):
        return obj.meeting_date.strftime("%b %d, %Y %I:%M %p")
    meeting_date_display.short_description = 'Meeting Date'
    meeting_date_display.admin_order_field = 'meeting_date'
    
    def status_display(self, obj):
        status_colors = {
            'scheduled': 'blue',
            'ongoing': 'orange',
            'completed': 'green',
            'cancelled': 'red',
            'postponed': 'gray'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            status_colors.get(obj.status, 'black'),
            obj.status
        )
    status_display.short_description = 'Status'
    
    def attendance_rate_display(self, obj):
        color = 'green' if obj.attendance_rate >= 70 else \
                'orange' if obj.attendance_rate >= 50 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color,
            obj.attendance_rate
        )
    attendance_rate_display.short_description = 'Attendance Rate'
    
    def qr_code_display(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="100" height="100" alt="QR Code" />',
                obj.qr_code.url
            )
        return "QR Code will be generated after saving"
    qr_code_display.short_description = 'QR Code'
    
    def is_upcoming_display(self, obj):
        if obj.is_upcoming:
            return format_html('<span style="color: green;"> Upcoming</span>')
        return format_html('<span style="color: gray;"> Not upcoming</span>')
    is_upcoming_display.short_description = 'Upcoming Meeting'
    
    def is_ongoing_display(self, obj):
        if obj.is_ongoing:
            return format_html('<span style="color: orange;"> Ongoing</span>')
        return format_html('<span style="color: gray;"> Not ongoing</span>')
    is_ongoing_display.short_description = 'Ongoing Meeting'

@admin.register(FarmerAttendance)
class FarmerAttendanceAdmin(admin.ModelAdmin):
    """Admin interface for detailed farmer attendance tracking"""
    
    list_display = [
        'farmer',
        'meeting_display',
        'attendance_status_display',
        'check_in_time_display',
        'checkin_method_display',
        'was_late_display'
    ]
    
    list_filter = [
        'attendance_status',
        'checkin_method', 
        'meeting__cbo_group',
        'meeting__meeting_date'
    ]
    
    search_fields = [
        'farmer__first_name',
        'farmer__last_name',
        'meeting__title'
    ]
    
    readonly_fields = ['duration_display', 'was_late_display']
    
    def meeting_display(self, obj):
        return f"{obj.meeting.cbo_group.name} - {obj.meeting.title}"
    meeting_display.short_description = 'Meeting'
    meeting_display.admin_order_field = 'meeting__title'
    
    def attendance_status_display(self, obj):
        status_colors = {
            'present': 'green',
            'absent': 'red', 
            'late': 'orange',
            'excused': 'blue'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            status_colors.get(obj.attendance_status, 'black'),
            obj.attendance_status
        )
    attendance_status_display.short_description = 'Status'
    
    def check_in_time_display(self, obj):
        if obj.check_in_time:
            return obj.check_in_time.strftime("%b %d, %Y %I:%M %p")
        return "Not checked in"
    check_in_time_display.short_description = 'Check-in Time'
    
    def checkin_method_display(self, obj):
        method_icons = {
            'qr_code': '',
            'manual': '',
            'biometric': '',
            'nfc': ''
        }
        return format_html(
            '{} {}',
            method_icons.get(obj.checkin_method, ''),
            obj.get_checkin_method_display()
        )
    checkin_method_display.short_description = 'Check-in Method'
    
    def was_late_display(self, obj):
        if obj.was_late:
            return format_html('<span style="color: orange;"> Late</span>')
        return format_html('<span style="color: green;"> On time</span>')
    was_late_display.short_description = 'Punctuality'
    
    def duration_display(self, obj):
        if obj.duration_minutes > 0:
            return f"{obj.duration_minutes:.1f} minutes"
        return "Not checked out"
    duration_display.short_description = 'Duration'

@admin.register(MeetingDocument)
class MeetingDocumentAdmin(admin.ModelAdmin):
    """Admin interface for meeting documents"""
    
    list_display = [
        'title',
        'meeting',
        'document_type_display',
        'uploaded_by',
        'created_at_display'
    ]
    
    list_filter = [
        'document_type',
        'meeting__cbo_group'
    ]
    
    def document_type_display(self, obj):
        type_colors = {
            'attendance_list': 'blue',
            'minutes': 'green',
            'presentation': 'purple',
            'photo': 'orange',
            'resolution': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            type_colors.get(obj.document_type, 'black'),
            obj.get_document_type_display()
        )
    document_type_display.short_description = 'Document Type'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime("%b %d, %Y")
    created_at_display.short_description = 'Uploaded Date'

@admin.register(CBOTraining)
class CBOTrainingAdmin(admin.ModelAdmin):
    """Admin interface for CBO training sessions"""
    
    list_display = [
        'title',
        'cbo_group',
        'training_category_display',
        'start_date_display',
        'duration_display',
        'total_participants',
        'evaluation_score_display'
    ]
    
    list_filter = [
        'training_category',
        'cbo_group__district'
    ]
    
    def training_category_display(self, obj):
        category_colors = {
            'agricultural': 'green',
            'financial': 'blue',
            'leadership': 'purple',
            'marketing': 'orange',
            'climate': 'teal',
            'technology': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            category_colors.get(obj.training_category, 'black'),
            obj.get_training_category_display()
        )
    training_category_display.short_description = 'Category'
    
    def start_date_display(self, obj):
        return obj.start_date.strftime("%b %d, %Y")
    start_date_display.short_description = 'Start Date'
    
    def duration_display(self, obj):
        return f"{obj.duration_hours:.1f} hours"
    duration_display.short_description = 'Duration'
    
    def evaluation_score_display(self, obj):
        if obj.evaluation_score:
            color = 'green' if obj.evaluation_score >= 4.0 else \
                    'orange' if obj.evaluation_score >= 3.0 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}/5</span>',
                color,
                obj.evaluation_score
            )
        return "Not evaluated"
    evaluation_score_display.short_description = 'Evaluation Score'
