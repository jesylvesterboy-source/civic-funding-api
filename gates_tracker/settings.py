"""
Django settings for gates_tracker project  PRODUCTION CONFIGURATION
Author: Jeremiah Williams Sylvester
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# --------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------
# SECURITY & ENVIRONMENT SETTINGS
# --------------------------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key-for-dev')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,.onrender.com').split(',')

# --------------------------------------
# CUSTOM USER MODEL
# --------------------------------------
AUTH_USER_MODEL = 'users.User'

# --------------------------------------
# APPLICATION DEFINITION
# --------------------------------------
INSTALLED_APPS = [
    'users',
    'core',
    'staff_performance',
    'farmer_engagement',
    'video_calls',
      'dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'projects',
    'farmers',
    'finances',
    'indicators',
    'reports',
    'sales',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gates_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gates_tracker.wsgi.application'

# --------------------------------------
# DATABASE CONFIGURATION - RENDER COMPATIBLE
# --------------------------------------
# Use DATABASE_URL from environment (provided by Render)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production - Use Render's PostgreSQL database
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development - Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# --------------------------------------
# REST FRAMEWORK CONFIGURATION
# --------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

# --------------------------------------
# EMAIL CONFIGURATION
# --------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = f"FSSS Tracker <{EMAIL_HOST_USER or 'no-reply@fsss.ng'}>"

# --------------------------------------
# SECURITY SETTINGS
# --------------------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
X_FRAME_OPTIONS = 'DENY'

# --------------------------------------
# CORS SETTINGS
# --------------------------------------
CORS_ALLOWED_ORIGINS = [
    "https://fsss.ng",
    "https://www.fsss.ng",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CSRF_TRUSTED_ORIGINS = [
    "https://fsss.ng",
    "https://www.fsss.ng",
    "https://*.fsss.ng",
    "http://localhost:3000",
    "https://*.onrender.com",
]

# --------------------------------------
# STATIC & MEDIA FILES
# --------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ensure directories exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)

# --------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
        },
        'simple': {'format': '{levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'gates_tracker.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO'},
        'gates_tracker': {'handlers': ['console', 'file'], 'level': 'DEBUG'},
    },
}

# --------------------------------------
# INTERNATIONALIZATION
# --------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------
# CELERY CONFIGURATION
# --------------------------------------
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_TIME_LIMIT = 300

# Authentication settings
LOGIN_REDIRECT_URL = '/'  # FSSS Dashboard
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Authentication settings
LOGIN_REDIRECT_URL = '/'  # FSSS Dashboard
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'




