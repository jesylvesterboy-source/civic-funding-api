import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
import django
django.setup()

from django.db import connection

print('=== REMOVING FINANCES MIGRATION FROM HISTORY ===')
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app = 'finances' AND name = '0001_initial'")
    print('Removed finances.0001_initial from migration history')
    
    # Verify removal
    cursor.execute("SELECT app, name FROM django_migrations WHERE app = 'finances'")
    remaining = cursor.fetchall()
    print(f'Remaining finances migrations: {len(remaining)}')
