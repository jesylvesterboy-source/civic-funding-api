# farmer_engagement/signals.py
# Signal handlers for Farmer Engagement module

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CBOMeeting, FarmerAttendance

@receiver(post_save, sender=CBOMeeting)
def update_meeting_attendance_count(sender, instance, **kwargs):
    """
    Update actual attendance count when attendance records change
    """
    attendance_count = FarmerAttendance.objects.filter(
        meeting=instance, 
        attendance_status='present'
    ).count()
    
    if instance.actual_attendance != attendance_count:
        instance.actual_attendance = attendance_count
        # Avoid infinite recursion by using update method
        CBOMeeting.objects.filter(pk=instance.pk).update(
            actual_attendance=attendance_count
        )

@receiver(post_save, sender=FarmerAttendance)
def update_cbo_member_stats(sender, instance, **kwargs):
    """
    Update CBO group statistics when attendance records change
    """
    # This can be expanded to update member participation rates
    pass
