import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
django.setup()

from django.core.management import execute_from_command_line

print("Running migrations...")
execute_from_command_line(['manage.py', 'migrate'])
print("Migrations completed!")
