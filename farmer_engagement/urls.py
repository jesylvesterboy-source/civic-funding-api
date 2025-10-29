# farmer_engagement/urls.py
from django.urls import path
from . import views

app_name = 'farmer_engagement'

urlpatterns = [
    # Dashboard - WORKING
    path('', views.FarmerEngagementDashboard.as_view(), name='dashboard'),
    
    # CBO Groups - WORKING
    path('cbo-groups/', views.CBOGroupList.as_view(), name='cbo_group_list'),
    path('cbo-groups/<uuid:group_id>/', views.CBOGroupDetail.as_view(), name='cbo_group_detail'),
    path('cbo-groups/export/', views.export_cbo_groups, name='export_cbo_groups'),
    
    # Meetings - WORKING
    path('meetings/', views.MeetingList.as_view(), name='meeting_list'),
    path('meetings/<uuid:meeting_id>/', views.MeetingDetail.as_view(), name='meeting_detail'),
    path('meetings/export/', views.export_meetings, name='export_meetings'),
    
    # Attendance - WORKING
    path('attendance/export/', views.export_attendance, name='export_attendance'),
    
    # Reports - WORKING
    path('reports/attendance/', views.AttendanceReport.as_view(), name='attendance_report'),
    path('reports/engagement/', views.EngagementReport.as_view(), name='engagement_report'),
]
