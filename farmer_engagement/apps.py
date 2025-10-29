from django.apps import AppConfig

class FarmerEngagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farmer_engagement"
    verbose_name = "Farmer Engagement & CBO Management"
    
    def ready(self):
        # Import signals here to avoid circular imports
        import farmer_engagement.signals
