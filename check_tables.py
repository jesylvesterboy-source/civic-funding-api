import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
import django
django.setup()

from django.db import connection

print('=== EXISTING FINANCES TABLES ===')
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'finances_%'")
    tables = cursor.fetchall()
    for table in tables:
        print(f'- {table[0]}')
