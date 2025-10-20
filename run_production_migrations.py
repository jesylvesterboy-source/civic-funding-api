#!/usr/bin/env python
"""Migration runner for production deployment"""
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
django.setup()

def run_migrations():
    """Run all pending migrations"""
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    print("Migrations completed successfully!")

if __name__ == '__main__':
    run_migrations()
