# staff_performance/kpi_calculations.py
"""
Performance KPI Calculation System
Measures staff performance based on app engagement and activities
"""

from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from datetime import datetime, timedelta
from .models import StaffMember, PerformanceMetric
from farmer_engagement.models import CBOMeeting, FarmerAttendance
from video_calls.models import VideoCallSession, CallParticipant

class PerformanceKPICalculator:
    """Calculate performance KPIs based on staff engagement across all modules"""
    
    def __init__(self, staff_member):
        self.staff_member = staff_member
        self.period_start = timezone.now() - timedelta(days=30)  # Last 30 days
        self.period_end = timezone.now()
    
    def calculate_all_kpis(self):
        """Calculate all performance KPIs"""
        return {
            'farmer_engagement_score': self.calculate_farmer_engagement_score(),
            'meeting_facilitation_score': self.calculate_meeting_facilitation_score(),
            'attendance_management_score': self.calculate_attendance_management_score(),
            'video_call_engagement_score': self.calculate_video_call_engagement_score(),
            'app_usage_score': self.calculate_app_usage_score(),
            'data_quality_score': self.calculate_data_quality_score(),
            'overall_performance_score': self.calculate_overall_performance_score(),
        }
    
    def calculate_farmer_engagement_score(self):
        """KPI: Farmer engagement and CBO management"""
        # Number of CBO groups assigned
        cbo_groups_count = self.staff_member.assigned_cbo_groups.filter(status='active').count()
        
        # Farmer reach (total farmers in assigned CBOs)
        farmer_reach = self.staff_member.assigned_cbo_groups.filter(
            status='active'
        ).aggregate(total=Sum('total_members'))['total'] or 0
        
        # Engagement activities
        meetings_facilitated = self.staff_member.facilitated_meetings.filter(
            meeting_date__range=[self.period_start, self.period_end]
        ).count()
        
        # Score calculation (weighted)
        score = min(100, (
            (cbo_groups_count * 10) + 
            (min(farmer_reach, 500) / 5) +  # Cap at 500 farmers
            (meetings_facilitated * 15)
        ))
        
        return round(score, 2)
    
    def calculate_meeting_facilitation_score(self):
        """KPI: Meeting facilitation effectiveness"""
        meetings = self.staff_member.facilitated_meetings.filter(
            meeting_date__range=[self.period_start, self.period_end]
        )
        
        if not meetings.exists():
            return 0
        
        # Average attendance rate
        avg_attendance_rate = meetings.aggregate(
            avg_rate=Avg('actual_attendance') / Avg('expected_attendance') * 100
        )['avg_rate'] or 0
        
        # Meeting frequency (target: 2 meetings per week)
        meeting_count = meetings.count()
        target_meetings = 8  # 2 meetings/week * 4 weeks
        frequency_score = min(100, (meeting_count / target_meetings) * 100)
        
        # Timeliness (meetings held as scheduled)
        on_time_meetings = meetings.filter(status='completed').count()
        timeliness_score = (on_time_meetings / meeting_count) * 100 if meeting_count > 0 else 0
        
        overall_score = (avg_attendance_rate * 0.4) + (frequency_score * 0.3) + (timeliness_score * 0.3)
        return round(overall_score, 2)
    
    def calculate_attendance_management_score(self):
        """KPI: Digital attendance management"""
        meetings = self.staff_member.facilitated_meetings.filter(
            meeting_date__range=[self.period_start, self.period_end]
        )
        
        if not meetings.exists():
            return 0
        
        # QR code usage rate
        qr_meetings = meetings.filter(qr_code__isnull=False).count()
        qr_usage_rate = (qr_meetings / meetings.count()) * 100
        
        # Digital check-in rate
        digital_checkins = FarmerAttendance.objects.filter(
            meeting__in=meetings,
            checkin_method__in=['qr_code', 'biometric', 'nfc']
        ).count()
        total_checkins = FarmerAttendance.objects.filter(meeting__in=meetings).count()
        
        digital_rate = (digital_checkins / total_checkins) * 100 if total_checkins > 0 else 0
        
        # Data completeness
        complete_attendance = meetings.filter(actual_attendance__gt=0).count()
        completeness_rate = (complete_attendance / meetings.count()) * 100
        
        overall_score = (qr_usage_rate * 0.4) + (digital_rate * 0.4) + (completeness_rate * 0.2)
        return round(overall_score, 2)
    
    def calculate_video_call_engagement_score(self):
        """KPI: Video call usage and engagement"""
        # Hosted video calls
        hosted_calls = self.staff_member.hosted_video_calls.filter(
            scheduled_time__range=[self.period_start, self.period_end]
        ).count()
        
        # Participation in calls
        participated_calls = self.staff_member.video_call_participations.filter(
            join_time__range=[self.period_start, self.period_end]
        ).count()
        
        # Call completion rate
        completed_calls = self.staff_member.hosted_video_calls.filter(
            status='completed',
            scheduled_time__range=[self.period_start, self.period_end]
        ).count()
        completion_rate = (completed_calls / hosted_calls) * 100 if hosted_calls > 0 else 0
        
        # Participant engagement
        avg_participants = self.staff_member.hosted_video_calls.filter(
            scheduled_time__range=[self.period_start, self.period_end]
        ).aggregate(avg=Avg('participant_count'))['avg'] or 0
        
        score = min(100, (
            (hosted_calls * 10) +
            (participated_calls * 5) +
            (completion_rate * 0.5) +
            (avg_participants * 2)
        ))
        
        return round(score, 2)
    
    def calculate_app_usage_score(self):
        """KPI: Overall app engagement and usage"""
        # This would integrate with actual app usage analytics
        # For now, using proxy metrics
        
        # Activity across modules
        farmer_activities = self.staff_member.facilitated_meetings.filter(
            meeting_date__range=[self.period_start, self.period_end]
        ).count()
        
        video_activities = self.staff_member.video_call_participations.filter(
            join_time__range=[self.period_start, self.period_end]
        ).count()
        
        performance_activities = self.staff_member.performance_reviews.filter(
            review_date__range=[self.period_start, self.period_end]
        ).count()
        
        total_activities = farmer_activities + video_activities + performance_activities
        
        # Daily activity consistency
        active_days = set()
        # Add logic to track active days across modules
        
        consistency_score = min(100, (len(active_days) / 30) * 100)  # 30-day period
        
        overall_score = min(100, (total_activities * 2) + (consistency_score * 0.5))
        return round(overall_score, 2)
    
    def calculate_data_quality_score(self):
        """KPI: Data accuracy and completeness"""
        meetings = self.staff_member.facilitated_meetings.filter(
            meeting_date__range=[self.period_start, self.period_end]
        )
        
        if not meetings.exists():
            return 0
        
        # Meeting documentation completeness
        documented_meetings = meetings.filter(
            Q(minutes__isnull=False) & ~Q(minutes='')
        ).count()
        documentation_rate = (documented_meetings / meetings.count()) * 100
        
        # Attendance data accuracy
        accurate_attendance = meetings.filter(
            actual_attendance__lte=F('expected_attendance')
        ).count()
        accuracy_rate = (accurate_attendance / meetings.count()) * 100
        
        # Timely data entry (within 24 hours)
        timely_entries = meetings.filter(
            created_at__lte=F('meeting_date') + timedelta(hours=24)
        ).count()
        timeliness_rate = (timely_entries / meetings.count()) * 100
        
        overall_score = (documentation_rate * 0.4) + (accuracy_rate * 0.4) + (timeliness_rate * 0.2)
        return round(overall_score, 2)
    
    def calculate_overall_performance_score(self):
        """Calculate weighted overall performance score"""
        kpis = self.calculate_all_kpis()
        
        # Weighted average of all KPIs
        weights = {
            'farmer_engagement_score': 0.25,
            'meeting_facilitation_score': 0.20,
            'attendance_management_score': 0.15,
            'video_call_engagement_score': 0.15,
            'app_usage_score': 0.15,
            'data_quality_score': 0.10,
        }
        
        weighted_score = sum(kpis[kpi] * weight for kpi, weight in weights.items())
        return round(weighted_score, 2)

def update_staff_performance_scores():
    """Update performance scores for all active staff members"""
    active_staff = StaffMember.objects.filter(is_active=True)
    
    for staff in active_staff:
        calculator = PerformanceKPICalculator(staff)
        kpis = calculator.calculate_all_kpis()
        
        # Update overall performance score
        staff.overall_performance_score = kpis['overall_performance_score']
        staff.save()
        
        # Create/update performance metrics
        for kpi_name, score in kpis.items():
            if kpi_name != 'overall_performance_score':
                PerformanceMetric.objects.update_or_create(
                    staff=staff,
                    metric_name=kpi_name,
                    period_end=timezone.now().date(),
                    defaults={
                        'metric_category': 'productivity',
                        'target_value': 100,
                        'actual_value': score,
                        'achievement_rate': score,
                        'period_start': timezone.now().date() - timedelta(days=30),
                    }
                )
