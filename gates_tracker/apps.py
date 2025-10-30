from django.apps import AppConfig

class GatesTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gates_tracker'
    verbose_name = 'Gates Tracker Enterprise'
    
    def ready(self):
        # Import signals and other startup code here
        try:
            import gates_tracker.signals  # noqa F401
        except ImportError:
            pass
