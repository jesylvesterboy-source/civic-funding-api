import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
import django
django.setup()

from django.db import connection

print('=== CURRENT MIGRATION HISTORY ===')
with connection.cursor() as cursor:
    cursor.execute("SELECT app, name FROM django_migrations WHERE app IN ('projects', 'finances') ORDER BY id")
    rows = cursor.fetchall()
    for row in rows:
        print(f'{row[0]}: {row[1]}')
