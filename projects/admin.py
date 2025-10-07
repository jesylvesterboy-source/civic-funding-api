from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'status', 'start_date', 'end_date', 'budget', 'project_manager']
    list_filter = ['status', 'country', 'donor']
    search_fields = ['name', 'code', 'description']
    list_editable = ['status']
    date_hierarchy = 'start_date'