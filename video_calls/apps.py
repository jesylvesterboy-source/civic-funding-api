from django.apps import AppConfig

class VideoCallsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "video_calls"
    verbose_name = "Video & Voice Calls"
    
    def ready(self):
        # Import signals here to avoid circular imports
        import video_calls.signals
