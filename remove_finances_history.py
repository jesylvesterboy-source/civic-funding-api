import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
import django
django.setup()

from django.db import connection

print('=== REMOVING FINANCES MIGRATION HISTORY ===')
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app = 'finances'")
    print('Removed all finances migrations from history')
