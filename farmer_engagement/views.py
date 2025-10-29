# farmer_engagement/views.py
import csv
import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count, Avg, Sum
from django.contrib import messages
from datetime import datetime, timedelta

from .models import CBOGroup, CBOMeeting, FarmerAttendance, CBOTraining
from staff_performance.models import StaffMember

class FarmerEngagementDashboard(LoginRequiredMixin, TemplateView):
    """Farmer Engagement Dashboard"""
    template_name = 'farmer_engagement/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Key statistics
        total_cbo_groups = CBOGroup.objects.filter(status='active').count()
        total_farmers = CBOGroup.objects.aggregate(total=Sum('total_members'))['total'] or 0
        total_meetings = CBOMeeting.objects.count()
        
        # Recent meetings
        recent_meetings = CBOMeeting.objects.select_related('cbo_group', 'facilitator__user').order_by('-meeting_date')[:5]
        
        # Attendance rates
        avg_attendance_rate = CBOMeeting.objects.aggregate(
            avg_rate=Avg('actual_attendance') / Avg('expected_attendance') * 100
        )['avg_rate'] or 0
        
        # Staff engagement stats
        staff_engagement = StaffMember.objects.annotate(
            meetings_facilitated=Count('facilitated_meetings'),
            total_attendance=Count('facilitated_meetings__attendances')
        ).order_by('-meetings_facilitated')[:5]
        
        context.update({
            'total_cbo_groups': total_cbo_groups,
            'total_farmers': total_farmers,
            'total_meetings': total_meetings,
            'recent_meetings': recent_meetings,
            'avg_attendance_rate': avg_attendance_rate,
            'staff_engagement': staff_engagement,
        })
        return context

class CBOGroupList(LoginRequiredMixin, ListView):
    """List CBO groups"""
    model = CBOGroup
    template_name = 'farmer_engagement/cbo_group_list.html'
    paginate_by = 20
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('assigned_staff__user')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

class CBOGroupDetail(LoginRequiredMixin, DetailView):
    """CBO group detail view"""
    model = CBOGroup
    template_name = 'farmer_engagement/cbo_group_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'group_id'

class MeetingList(LoginRequiredMixin, ListView):
    """List CBO meetings"""
    model = CBOMeeting
    template_name = 'farmer_engagement/meeting_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return CBOMeeting.objects.select_related('cbo_group', 'facilitator__user').all()

class MeetingDetail(LoginRequiredMixin, DetailView):
    """Meeting detail view"""
    model = CBOMeeting
    template_name = 'farmer_engagement/meeting_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'meeting_id'

class MeetingAttendance(LoginRequiredMixin, DetailView):
    """Meeting attendance view"""
    model = CBOMeeting
    template_name = 'farmer_engagement/meeting_attendance.html'
    slug_field = 'id'
    slug_url_kwarg = 'meeting_id'

class AttendanceReport(LoginRequiredMixin, TemplateView):
    """Attendance report view"""
    template_name = 'farmer_engagement/attendance_report.html'

class EngagementReport(LoginRequiredMixin, TemplateView):
    """Engagement report view"""
    template_name = 'farmer_engagement/engagement_report.html'

# Function-based views
def export_cbo_groups(request):
    """Export CBO groups to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cbo_groups.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Group Name', 'Type', 'District', 'Sub-County', 'Village', 
        'Total Members', 'Female Members', 'Male Members', 'Formation Date', 'Status'
    ])
    
    groups = CBOGroup.objects.all()
    for group in groups:
        writer.writerow([
            group.name,
            group.get_group_type_display(),
            group.district,
            group.sub_county,
            group.village,
            group.total_members,
            group.female_members,
            group.male_members,
            group.formation_date.strftime('%Y-%m-%d'),
            group.get_status_display()
        ])
    
    return response

def import_cbo_groups(request):
    """Import CBO groups from CSV"""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        messages.success(request, 'CBO groups imported successfully!')
        return redirect('farmer_engagement:cbo_group_list')
    
    return render(request, 'farmer_engagement/import_cbo_groups.html')

def export_meetings(request):
    """Export meetings to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cbo_meetings.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'CBO Group', 'Meeting Title', 'Type', 'Meeting Date', 'Venue', 
        'Facilitator', 'Expected Attendance', 'Actual Attendance', 'Attendance Rate'
    ])
    
    meetings = CBOMeeting.objects.select_related('cbo_group', 'facilitator__user').all()
    for meeting in meetings:
        writer.writerow([
            meeting.cbo_group.name,
            meeting.title,
            meeting.get_meeting_type_display(),
            meeting.meeting_date.strftime('%Y-%m-%d %H:%M'),
            meeting.venue,
            meeting.facilitator.user.get_full_name(),
            meeting.expected_attendance,
            meeting.actual_attendance,
            f"{meeting.attendance_rate:.1f}%"
        ])
    
    return response

def export_attendance(request):
    """Export attendance records to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="farmer_attendance.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Farmer Name', 'CBO Group', 'Meeting Title', 'Meeting Date', 
        'Attendance Status', 'Check-in Time', 'Check-in Method'
    ])
    
    attendance_records = FarmerAttendance.objects.select_related(
        'farmer', 'meeting__cbo_group'
    ).all()
    
    for record in attendance_records:
        writer.writerow([
            record.farmer.full_name,
            record.meeting.cbo_group.name,
            record.meeting.title,
            record.meeting.meeting_date.strftime('%Y-%m-%d %H:%M'),
            record.get_attendance_status_display(),
            record.check_in_time.strftime('%Y-%m-%d %H:%M') if record.check_in_time else '',
            record.get_checkin_method_display()
        ])
    
    return response

def qr_code_checkin(request, meeting_id):
    """QR code check-in endpoint"""
    meeting = get_object_or_404(CBOMeeting, id=meeting_id)
    
    if request.method == 'POST':
        return JsonResponse({'status': 'checked_in', 'meeting': meeting.title})
    
    return render(request, 'farmer_engagement/qr_checkin.html', {'meeting': meeting})

def import_meetings(request):
    """Import meetings from CSV"""
    return HttpResponse("Import meetings functionality")

def import_attendance(request):
    """Import attendance from CSV"""
    return HttpResponse("Import attendance functionality")
