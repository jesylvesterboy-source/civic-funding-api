from django.contrib import admin
from .models import Report, MonitoringVisit

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['project', 'report_type', 'reporting_period_start', 'reporting_period_end', 'submitted_by', 'verified']
    list_filter = ['report_type', 'verified', 'submission_date']
    search_fields = ['project__name', 'summary']
    date_hierarchy = 'submission_date'

@admin.register(MonitoringVisit)
class MonitoringVisitAdmin(admin.ModelAdmin):
    list_display = ['project', 'visit_date', 'visited_by', 'follow_up_required']
    list_filter = ['visit_date', 'follow_up_required']
    search_fields = ['project__name', 'purpose', 'findings']
    date_hierarchy = 'visit_date'