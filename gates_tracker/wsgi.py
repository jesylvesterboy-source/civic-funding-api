# gates_tracker/wsgi.py
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.production_settings')

application = get_wsgi_application()
application = WhiteNoise(application, root='staticfiles')
