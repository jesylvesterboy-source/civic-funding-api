# video_calls/urls.py
from django.urls import path
from . import views

app_name = 'video_calls'

urlpatterns = [
    # Video Call Dashboard - WORKING
    path('', views.VideoCallDashboard.as_view(), name='dashboard'),
    
    # Session Management - WORKING
    path('sessions/', views.VideoCallList.as_view(), name='session_list'),
    path('sessions/<uuid:session_id>/', views.VideoCallDetail.as_view(), name='session_detail'),
    
    # Video Room URLs - WORKING
    path('room/<str:session_id>/', views.VideoCallRoom.as_view(), name='video_room'),
    path('join/<str:session_id>/', views.JoinVideoCall.as_view(), name='join_session'),
    
    # Recording Management - WORKING
    path('recordings/', views.RecordingList.as_view(), name='recording_list'),
]
