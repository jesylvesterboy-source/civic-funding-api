from django.contrib import admin
from django.utils.html import format_html
from .models import (
    StaffMember, 
    PerformanceMetric, 
    KeyPerformanceIndicator,
    PerformanceReview, 
    StaffAchievement, 
    TrainingDevelopment
)

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    """Professional admin interface for Staff Member management"""
    
    list_display = [
        'employee_id', 
        'get_full_name', 
        'department', 
        'position_level', 
        'performance_score_display',
        'tenure_display',
        'is_active'
    ]
    
    list_filter = [
        'department', 
        'position_level', 
        'is_active',
        'created_at'
    ]
    
    search_fields = [
        'user__first_name', 
        'user__last_name', 
        'employee_id',
        'position_title'
    ]
    
    readonly_fields = ['tenure_display', 'performance_tier_display']
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'user', 
                'employee_id',
                'work_phone',
                'work_email'
            )
        }),
        ('Employment Details', {
            'fields': (
                'department',
                'position_title', 
                'position_level',
                'hire_date',
                'supervisor',
                'assigned_region'
            )
        }),
        ('Performance Metrics', {
            'fields': (
                'overall_performance_score',
                'last_performance_review',
                'tenure_display',
                'performance_tier_display'
            )
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
    
    def get_full_name(self, obj):
        return obj.full_name
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__last_name'
    
    def performance_score_display(self, obj):
        color = 'green' if obj.overall_performance_score >= 80 else \
                'orange' if obj.overall_performance_score >= 60 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            obj.overall_performance_score
        )
    performance_score_display.short_description = 'Performance Score'
    
    def tenure_display(self, obj):
        return f"{obj.tenure_months} months"
    tenure_display.short_description = 'Tenure'
    
    def performance_tier_display(self, obj):
        tier_colors = {
            'excellent': 'green',
            'very_good': 'blue', 
            'good': 'orange',
            'satisfactory': 'yellow',
            'needs_improvement': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            tier_colors.get(obj.performance_tier, 'black'),
            obj.performance_tier.replace('_', ' ')
        )
    performance_tier_display.short_description = 'Performance Tier'

@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    """Admin interface for individual performance metrics"""
    
    list_display = [
        'staff',
        'metric_name', 
        'metric_category',
        'target_value',
        'actual_value', 
        'achievement_rate_display',
        'period_end'
    ]
    
    list_filter = [
        'metric_category',
        'period_end',
        'staff__department'
    ]
    
    search_fields = [
        'staff__user__first_name',
        'staff__user__last_name',
        'metric_name'
    ]
    
    readonly_fields = ['achievement_rate_display']
    
    def achievement_rate_display(self, obj):
        color = 'green' if obj.achievement_rate >= 100 else \
                'orange' if obj.achievement_rate >= 80 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            obj.achievement_rate
        )
    achievement_rate_display.short_description = 'Achievement Rate'

@admin.register(KeyPerformanceIndicator)
class KeyPerformanceIndicatorAdmin(admin.ModelAdmin):
    """Admin interface for organizational KPIs"""
    
    list_display = [
        'name',
        'department',
        'kpi_type',
        'current_value',
        'target_value',
        'achievement_status',
        'last_updated'
    ]
    
    list_filter = [
        'department',
        'kpi_type',
        'reporting_frequency',
        'is_active'
    ]
    
    readonly_fields = ['achievement_status', 'last_updated']
    
    def achievement_status(self, obj):
        status_colors = {
            'exceeded': 'green',
            'achieved': 'blue',
            'moderate': 'orange',
            'needs_attention': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{} ({}%)</span>',
            status_colors.get(obj.status, 'black'),
            obj.status.replace('_', ' '),
            obj.achievement_percentage
        )
    achievement_status.short_description = 'Achievement Status'

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    """Admin interface for performance reviews"""
    
    list_display = [
        'staff',
        'review_type',
        'review_date',
        'overall_rating_display',
        'reviewer',
        'is_completed'
    ]
    
    list_filter = [
        'review_type',
        'review_date',
        'is_completed'
    ]
    
    readonly_fields = ['overall_rating_display']
    
    def overall_rating_display(self, obj):
        color = 'green' if obj.overall_rating >= 4.0 else \
                'blue' if obj.overall_rating >= 3.0 else \
                'orange' if obj.overall_rating >= 2.0 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}/5</span>',
            color,
            obj.overall_rating
        )
    overall_rating_display.short_description = 'Overall Rating'

@admin.register(StaffAchievement)
class StaffAchievementAdmin(admin.ModelAdmin):
    """Admin interface for staff achievements"""
    
    list_display = [
        'staff',
        'achievement_type',
        'title',
        'date_achieved',
        'recognizing_organization'
    ]
    
    list_filter = [
        'achievement_type',
        'date_achieved'
    ]

@admin.register(TrainingDevelopment)
class TrainingDevelopmentAdmin(admin.ModelAdmin):
    """Admin interface for training and development"""
    
    list_display = [
        'staff',
        'training_title',
        'training_type',
        'start_date',
        'end_date',
        'status_display',
        'training_rating'
    ]
    
    list_filter = [
        'training_type',
        'status',
        'start_date'
    ]
    
    def status_display(self, obj):
        status_colors = {
            'completed': 'green',
            'in_progress': 'blue',
            'planned': 'orange',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            status_colors.get(obj.status, 'black'),
            obj.status.replace('_', ' ')
        )
    status_display.short_description = 'Status'
