import os
import django
from django.core import serializers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
django.setup()

# Export all data to JSON
from django.apps import apps

print("🔍 Exporting database from Render...")
all_data = {}

for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        try:
            data = serializers.serialize("json", model.objects.all())
            all_data[model.__name__] = data
            print(f"✅ Exported {model.__name__}: {model.objects.count()} records")
        except Exception as e:
            print(f"⚠️  Could not export {model.__name__}: {e}")

# Save to file
import json
with open('render_backup.json', 'w') as f:
    json.dump(all_data, f)

print("🎉 Database export complete: render_backup.json")
