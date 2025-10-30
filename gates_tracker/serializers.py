from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

# User Management Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EnterpriseUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = EnterpriseUserProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

# Staff Performance Serializers
class KPICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = KPICategory
        fields = '__all__'

class PerformanceMetricSerializer(serializers.ModelSerializer):
    kpi_category_name = serializers.CharField(source='kpi_category.name', read_only=True)

    class Meta:
        model = PerformanceMetric
        fields = '__all__'

class StaffPerformanceSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.user.get_full_name', read_only=True)
    manager_name = serializers.CharField(source='manager.user.get_full_name', read_only=True)
    performance_cycle_name = serializers.CharField(source='performance_cycle.name', read_only=True)
    metrics = PerformanceMetricSerializer(many=True, read_only=True)

    class Meta:
        model = StaffPerformance
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

# Farmer Engagement Serializers
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CBOGroupSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = CBOGroup
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class FarmerSerializer(serializers.ModelSerializer):
    cbo_group_name = serializers.CharField(source='cbo_group.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Farmer
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'

class TrainingSessionSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.name', read_only=True)
    facilitator_names = serializers.SerializerMethodField()

    class Meta:
        model = TrainingSession
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_facilitator_names(self, obj):
        return [f.user.get_full_name() for f in obj.facilitators.all()]

class FarmerAttendanceSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.full_name', read_only=True)
    training_session_name = serializers.CharField(source='training_session.program.name', read_only=True)
    session_date = serializers.DateField(source='training_session.session_date', read_only=True)

    class Meta:
        model = FarmerAttendance
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

# Video Calls Serializers
class VideoCallSessionSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.user.get_full_name', read_only=True)
    participant_count = serializers.IntegerField(source='participants.count', read_only=True)

    class Meta:
        model = VideoCallSession
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CallParticipantSerializer(serializers.ModelSerializer):
    participant_name = serializers.CharField(source='participant.user.get_full_name', read_only=True)
    call_title = serializers.CharField(source='call_session.title', read_only=True)

    class Meta:
        model = CallParticipant
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class CallAnalyticsSerializer(serializers.ModelSerializer):
    call_title = serializers.CharField(source='call_session.title', read_only=True)

    class Meta:
        model = CallAnalytics
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

# Analytics and Reporting Serializers
class DashboardSnapshotSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.user.get_full_name', read_only=True)

    class Meta:
        model = DashboardSnapshot
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user.get_full_name', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

# Dashboard Statistics Serializer
class DashboardStatsSerializer(serializers.Serializer):
    total_staff = serializers.IntegerField()
    active_staff = serializers.IntegerField()
    total_farmers = serializers.IntegerField()
    active_farmers = serializers.IntegerField()
    total_cbo_groups = serializers.IntegerField()
    video_calls_today = serializers.IntegerField()
    training_sessions_this_month = serializers.IntegerField()
    average_performance_score = serializers.DecimalField(max_digits=5, decimal_places=2)
    engagement_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    
    performance_trend = serializers.ListField(child=serializers.DecimalField(max_digits=5, decimal_places=2))
    engagement_distribution = serializers.DictField(child=serializers.IntegerField())
    recent_activities = serializers.ListField(child=serializers.DictField())
