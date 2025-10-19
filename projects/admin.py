from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'status', 'start_date', 'end_date', 'budget', 'progress']
    list_filter = ['status', 'is_active']
    search_fields = ['name', 'code', 'description']
    list_editable = ['status', 'progress']
    date_hierarchy = 'start_date'
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'status', 'progress')
        }),
        ('Financial Information', {
            'fields': ('budget',)
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'actual_start_date', 'actual_end_date')
        }),
        ('Management', {
            'fields': ('manager', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('objectives', 'success_criteria', 'risks', 'notes'),
            'classes': ('collapse',)
        }),
    )
