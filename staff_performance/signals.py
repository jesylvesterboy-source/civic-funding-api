# staff_performance/signals.py
# Signal handlers for Staff Performance module

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import StaffMember

@receiver(post_save, sender=get_user_model())
def create_staff_profile(sender, instance, created, **kwargs):
    """
    Automatically create StaffMember profile when User is created
    """
    if created and hasattr(instance, 'email'):
        # Only create for users with email (staff members)
        StaffMember.objects.get_or_create(
            user=instance,
            defaults={
                'employee_id': f"EMP{instance.id:06d}",
                'department': 'field_operations',
                'position_title': 'Staff Member',
                'position_level': 'officer'
            }
        )

@receiver(post_save, sender=StaffMember)
def update_performance_score(sender, instance, **kwargs):
    """
    Recalculate overall performance score when metrics change
    """
    # This will be implemented when we have performance calculations
    pass
