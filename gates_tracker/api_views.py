from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .serializers import *

# Base Enterprise ViewSet with Common Functionality
class EnterpriseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    
    def get_queryset(self):
        return super().get_queryset().select_related()

# User Management API
class DepartmentViewSet(EnterpriseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ['is_active']

class EnterpriseUserProfileViewSet(EnterpriseViewSet):
    queryset = EnterpriseUserProfile.objects.select_related('user', 'department')
    serializer_class = EnterpriseUserProfileSerializer
    filterset_fields = ['department', 'role', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']

    @action(detail=False, methods=['get'])
    def active_users(self, request):
        active_users = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)

# Staff Performance API
class StaffPerformanceViewSet(EnterpriseViewSet):
    queryset = StaffPerformance.objects.select_related(
        'staff__user', 'manager__user', 'performance_cycle'
    ).prefetch_related('metrics__kpi_category')
    serializer_class = StaffPerformanceSerializer
    filterset_fields = ['performance_cycle', 'status']
    search_fields = ['staff__user__first_name', 'staff__user__last_name']

    @action(detail=False, methods=['get'])
    def performance_stats(self, request):
        stats = {
            'total_evaluations': StaffPerformance.objects.count(),
            'average_score': StaffPerformance.objects.aggregate(
                avg_score=Avg('overall_score')
            )['avg_score'] or 0,
            'completed_evaluations': StaffPerformance.objects.filter(status='approved').count(),
            'pending_evaluations': StaffPerformance.objects.filter(status__in=['draft', 'submitted']).count(),
        }
        return Response(stats)

# Farmer Engagement API
class FarmerViewSet(EnterpriseViewSet):
    queryset = Farmer.objects.select_related('cbo_group', 'region')
    serializer_class = FarmerSerializer
    filterset_fields = ['region', 'cbo_group', 'gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'farmer_id', 'phone_number']

    @action(detail=False, methods=['get'])
    def engagement_stats(self, request):
        total_farmers = Farmer.objects.count()
        active_farmers = Farmer.objects.filter(is_active=True).count()
        recent_engagement = Farmer.objects.filter(
            last_engagement_date__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        stats = {
            'total_farmers': total_farmers,
            'active_farmers': active_farmers,
            'engagement_rate': (recent_engagement / active_farmers * 100) if active_farmers > 0 else 0,
            'by_region': list(Farmer.objects.values('region__name').annotate(count=Count('id'))),
        }
        return Response(stats)

class TrainingSessionViewSet(EnterpriseViewSet):
    queryset = TrainingSession.objects.select_related('program').prefetch_related('facilitators__user')
    serializer_class = TrainingSessionSerializer
    filterset_fields = ['program', 'session_date']
    search_fields = ['program__name', 'location']

# Video Calls API
class VideoCallSessionViewSet(EnterpriseViewSet):
    queryset = VideoCallSession.objects.select_related('organizer__user').prefetch_related('participants__participant__user')
    serializer_class = VideoCallSessionSerializer
    filterset_fields = ['call_type', 'status']
    search_fields = ['title', 'organizer__user__first_name']

    @action(detail=False, methods=['get'])
    def today_calls(self, request):
        today = timezone.now().date()
        today_calls = self.get_queryset().filter(scheduled_start__date=today)
        serializer = self.get_serializer(today_calls, many=True)
        return Response(serializer.data)

# Dashboard API
class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Real data calculations
        total_staff = EnterpriseUserProfile.objects.count()
        active_staff = EnterpriseUserProfile.objects.filter(is_active=True).count()
        total_farmers = Farmer.objects.count()
        active_farmers = Farmer.objects.filter(is_active=True).count()
        total_cbo_groups = CBOGroup.objects.count()
        
        today = timezone.now().date()
        video_calls_today = VideoCallSession.objects.filter(
            scheduled_start__date=today, 
            status='completed'
        ).count()
        
        training_sessions_this_month = TrainingSession.objects.filter(
            session_date__month=today.month,
            session_date__year=today.year
        ).count()
        
        average_performance = StaffPerformance.objects.filter(
            status='approved'
        ).aggregate(avg_score=Avg('overall_score'))['avg_score'] or 0
        
        # Engagement rate calculation
        engaged_farmers = Farmer.objects.filter(
            last_engagement_date__gte=timezone.now() - timedelta(days=30)
        ).count()
        engagement_rate = (engaged_farmers / active_farmers * 100) if active_farmers > 0 else 0
        
        # Performance trend (last 7 days)
        performance_trend = [85, 82, 88, 90, 87, 85, 89]  # Placeholder - would be real calculations
        
        # Engagement distribution
        engagement_distribution = {
            'Farmers': active_farmers,
            'CBO Groups': total_cbo_groups,
            'Active Projects': CBOGroup.objects.filter(is_active=True).count(),
            'Training Sessions': training_sessions_this_month,
        }
        
        # Recent activities
        recent_activities = [
            {
                'module': 'Staff Performance',
                'action': f'{active_staff} active staff members',
                'time': 'Live'
            },
            {
                'module': 'Farmer Engagement', 
                'action': f'{active_farmers} farmers engaged',
                'time': 'Live'
            },
            {
                'module': 'Video Calls',
                'action': f'{video_calls_today} calls completed today',
                'time': 'Live'
            },
        ]
        
        stats = {
            'total_staff': total_staff,
            'active_staff': active_staff,
            'total_farmers': total_farmers,
            'active_farmers': active_farmers,
            'total_cbo_groups': total_cbo_groups,
            'video_calls_today': video_calls_today,
            'training_sessions_this_month': training_sessions_this_month,
            'average_performance_score': round(float(average_performance), 2),
            'engagement_rate': round(engagement_rate, 2),
            'performance_trend': performance_trend,
            'engagement_distribution': engagement_distribution,
            'recent_activities': recent_activities,
        }
        
        return Response(stats)

# System Configuration API
class SystemConfigurationViewSet(EnterpriseViewSet):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfiguration.Serializer
    permission_classes = [IsAdminUser]

# Audit Log API (Read-only)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user__user')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['action_type', 'model_name']
    search_fields = ['user__user__first_name', 'user__user__last_name', 'description']
