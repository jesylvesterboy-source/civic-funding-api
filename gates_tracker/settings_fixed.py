# gates_tracker/settings.py (corrected authentication section)
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Lagos'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_TIME_LIMIT = 300

# Authentication settings - FIXED: Redirect to FSSS Dashboard
LOGIN_REDIRECT_URL = '/'  # Changed from '/users/dashboard/' to our FSSS dashboard
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
