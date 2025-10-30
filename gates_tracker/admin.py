from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Department, EnterpriseUserProfile, PerformanceCycle, 
    KPICategory, StaffPerformance, PerformanceMetric,
    Region, CBOGroup, Farmer, DashboardSnapshot, AuditLog
)

# Enterprise Admin Site Configuration
admin.site.site_header = 'Gates Tracker Enterprise Administration'
admin.site.site_title = 'Enterprise Admin Portal'
admin.site.index_title = 'Enterprise Data Management'

# Inline Admin Classes
class EnterpriseUserProfileInline(admin.StackedInline):
    model = EnterpriseUserProfile
    can_delete = False
    verbose_name_plural = 'Enterprise Profile'

class UserAdminWithProfile(UserAdmin):
    inlines = (EnterpriseUserProfileInline,)

# Professional Admin Classes
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(EnterpriseUserProfile)
class EnterpriseUserProfileAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user_full_name', 'department', 'role', 'is_active']
    list_filter = ['department', 'role', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Full Name'

@admin.register(PerformanceCycle)
class PerformanceCycleAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date']

@admin.register(StaffPerformance)
class StaffPerformanceAdmin(admin.ModelAdmin):
    list_display = ['staff', 'performance_cycle', 'overall_score', 'evaluation_date', 'status']
    list_filter = ['performance_cycle', 'status', 'evaluation_date']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'population', 'is_active']
    list_filter = ['is_active']

@admin.register(CBOGroup)
class CBOGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'group_id', 'group_type', 'region', 'total_members', 'is_active']
    list_filter = ['group_type', 'region', 'is_active']

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['farmer_id', 'full_name', 'gender', 'cbo_group', 'region', 'is_active']
    list_filter = ['gender', 'region', 'cbo_group', 'is_active']

@admin.register(DashboardSnapshot)
class DashboardSnapshotAdmin(admin.ModelAdmin):
    list_display = ['snapshot_id', 'snapshot_date', 'generated_by']
    readonly_fields = ['snapshot_id']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'model_name', 'object_id', 'created_at']
    list_filter = ['action_type', 'model_name']
    readonly_fields = ['created_at']

# Safe UserAdmin re-registration with error handling
try:
    admin.site.unregister(User)
    admin.site.register(User, UserAdminWithProfile)
except admin.sites.NotRegistered:
    # User model was never registered, so register it directly
    admin.site.register(User, UserAdminWithProfile)
