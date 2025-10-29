from django.apps import AppConfig

class StaffPerformanceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staff_performance"
    verbose_name = "Staff Performance Tracking"
    
    def ready(self):
        # Import signals here to avoid circular imports
        import staff_performance.signals
