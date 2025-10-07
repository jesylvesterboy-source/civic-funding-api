import os
from celery import Celery
from django.conf import settings

# --------------------------------------
# DEFAULT DJANGO SETTINGS MODULE
# --------------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')

# --------------------------------------
# CREATE CELERY APP INSTANCE
# --------------------------------------
app = Celery('gates_tracker')

# Load Celery configuration from Django settings using the CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed Django apps
app.autodiscover_tasks()


# --------------------------------------
# DEBUG / TEST TASK
# --------------------------------------
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# --------------------------------------
# OPTIONAL: FALLBACK / INLINE CONFIG (if environment variables not loaded)
# --------------------------------------
app.conf.update(
    broker_url=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND', 'django-db'),
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='Africa/Lagos',
    broker_connection_retry_on_startup=True,
)
