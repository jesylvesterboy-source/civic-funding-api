# gates_tracker/production_settings.py
import os
import dj_database_url
from decouple import config
from .settings import *

# Security settings for production
DEBUG = False
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# Database configuration for Render - using pg8000 adapter
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# Alternative: Use dj_database_url with pg8000
# Parse DATABASE_URL and manually set the engine
import urllib.parse
if 'DATABASE_URL' in os.environ:
    db_url = os.environ['DATABASE_URL']
    parsed = urllib.parse.urlparse(db_url)
    
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed.path[1:],
        'USER': parsed.username,
        'PASSWORD': parsed.password,
        'HOST': parsed.hostname,
        'PORT': parsed.port or '5432',
    }

# Static files configuration for Render
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# CORS settings (if needed)
CORS_ALLOWED_ORIGINS = [
    "https://fsss-platform.onrender.com",
]
