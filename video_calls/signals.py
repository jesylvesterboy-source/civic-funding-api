# video_calls/signals.py
# Signal handlers for Video Calls module

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import VideoCallSession, CallParticipant, CallRecording

@receiver(pre_save, sender=VideoCallSession)
def generate_room_url(sender, instance, **kwargs):
    """
    Generate WebRTC room URL when video call session is created
    """
    if not instance.room_url and instance.session_id:
        instance.room_url = f"/video/room/{instance.session_id}/"

@receiver(post_save, sender=CallParticipant)
def update_session_participant_count(sender, instance, **kwargs):
    """
    Update participant count and session status when participants join/leave
    """
    session = instance.session
    
    # Update session status based on participants
    active_participants = session.participants.filter(left_at__isnull=True).count()
    
    if active_participants > 0 and session.status != 'active':
        session.status = 'active'
        if not session.actual_start_time:
            session.actual_start_time = timezone.now()
        session.save()
    elif active_participants == 0 and session.status == 'active':
        session.status = 'completed'
        session.actual_end_time = timezone.now()
        
        # Calculate duration
        if session.actual_start_time and session.actual_end_time:
            duration = session.actual_end_time - session.actual_start_time
            session.duration_minutes = duration.total_seconds() / 60
        
        session.save()

@receiver(post_save, sender=CallRecording)
def update_recording_duration(sender, instance, **kwargs):
    """
    Calculate recording duration when start and end times are set
    """
    if instance.start_time and instance.end_time:
        duration = instance.end_time - instance.start_time
        instance.duration_seconds = duration.total_seconds()
        
        # Avoid infinite recursion by using update
        CallRecording.objects.filter(pk=instance.pk).update(
            duration_seconds=instance.duration_seconds
        )
