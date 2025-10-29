# video_calls/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from .models import VideoCallSession, CallParticipant, CallRecording, VideoCallSettings
from staff_performance.models import StaffMember

class VideoCallDashboard(LoginRequiredMixin, TemplateView):
    """Video Call Dashboard for staff members"""
    template_name = 'video_calls/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_member = get_object_or_404(StaffMember, user=self.request.user)
        
        # Get upcoming calls
        upcoming_calls = VideoCallSession.objects.filter(
            scheduled_time__gte=timezone.now(),
            status='scheduled'
        ).order_by('scheduled_time')[:5]
        
        # Get active calls
        active_calls = VideoCallSession.objects.filter(
            status='active'
        ).order_by('-actual_start_time')[:5]
        
        # Get user's scheduled calls
        user_calls = VideoCallSession.objects.filter(
            host=staff_member
        ).order_by('-scheduled_time')[:10]
        
        context.update({
            'staff_member': staff_member,
            'upcoming_calls': upcoming_calls,
            'active_calls': active_calls,
            'user_calls': user_calls,
            'total_calls_hosted': VideoCallSession.objects.filter(host=staff_member).count(),
        })
        return context

class VideoCallList(LoginRequiredMixin, ListView):
    """List all video call sessions"""
    model = VideoCallSession
    template_name = 'video_calls/session_list.html'
    paginate_by = 20
    ordering = ['-scheduled_time']
    
    def get_queryset(self):
        return VideoCallSession.objects.select_related('host__user').all()

class VideoCallDetail(LoginRequiredMixin, DetailView):
    """Detail view for a video call session"""
    model = VideoCallSession
    template_name = 'video_calls/session_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'session_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.object
        
        # Get participants
        participants = session.participants.select_related('staff_member__user').all()
        
        context.update({
            'participants': participants,
            'can_join': self.can_join_session(session),
            'is_host': session.host.user == self.request.user,
        })
        return context
    
    def can_join_session(self, session):
        """Check if user can join the session"""
        if session.status in ['active', 'scheduled']:
            if session.is_public:
                return True
            staff_member = get_object_or_404(StaffMember, user=self.request.user)
            return staff_member in session.co_hosts.all() or session.host == staff_member
        return False

class VideoCallRoom(LoginRequiredMixin, TemplateView):
    """Main video call room with WebRTC interface"""
    template_name = 'video_calls/video_room.html'
    
    def get(self, request, *args, **kwargs):
        session_id = kwargs.get('session_id')
        session = get_object_or_404(VideoCallSession, session_id=session_id)
        
        # Check if user can join
        staff_member = get_object_or_404(StaffMember, user=request.user)
        if not session.is_public and staff_member not in session.co_hosts.all() and session.host != staff_member:
            messages.error(request, 'You do not have permission to join this call.')
            return redirect('video_calls:dashboard')
        
        # Update session status if needed
        if session.status == 'scheduled':
            session.status = 'active'
            if not session.actual_start_time:
                session.actual_start_time = timezone.now()
            session.save()
        
        # Create or update participant record
        participant, created = CallParticipant.objects.get_or_create(
            session=session,
            staff_member=staff_member,
            defaults={
                'join_time': timezone.now(),
                'role': 'co_host' if staff_member in session.co_hosts.all() else 'participant'
            }
        )
        
        if not created and participant.left_at:
            participant.join_time = timezone.now()
            participant.left_at = None
            participant.save()
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = kwargs.get('session_id')
        session = get_object_or_404(VideoCallSession, session_id=session_id)
        staff_member = get_object_or_404(StaffMember, user=self.request.user)
        
        context.update({
            'session': session,
            'staff_member': staff_member,
            'participants': session.participants.filter(left_at__isnull=True).select_related('staff_member__user'),
            'is_host': session.host == staff_member,
        })
        return context

class JoinVideoCall(LoginRequiredMixin, View):
    """Join a video call with access control"""
    
    def get(self, request, session_id):
        session = get_object_or_404(VideoCallSession, session_id=session_id)
        staff_member = get_object_or_404(StaffMember, user=request.user)
        
        # Check access permissions
        if not session.is_public and staff_member not in session.co_hosts.all() and session.host != staff_member:
            messages.error(request, 'You do not have permission to join this call.')
            return redirect('video_calls:dashboard')
        
        # Check if call is active or scheduled
        if session.status not in ['active', 'scheduled']:
            messages.error(request, 'This call is not currently active.')
            return redirect('video_calls:dashboard')
        
        # Redirect to video room
        return redirect('video_calls:video_room', session_id=session_id)

class RecordingList(LoginRequiredMixin, ListView):
    """List all call recordings"""
    model = CallRecording
    template_name = 'video_calls/recording_list.html'
    paginate_by = 20
    ordering = ['-start_time']
