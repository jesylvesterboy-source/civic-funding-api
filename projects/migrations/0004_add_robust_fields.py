# Create a safe migration that checks if field exists
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

def safe_add_project_manager(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    field_names = [f.name for f in Project._meta.get_fields()]
    
    # Only add field if it doesn't exist
    if 'project_manager' not in field_names:
        field = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=django.db.models.deletion.SET_NULL,
            null=True,
            blank=True,
            related_name='project_managed_projects',
            verbose_name='Project Manager'
        )
        field.contribute_to_class(Project, 'project_manager')

class Migration(migrations.Migration):
    dependencies = [
        ('projects', '0003_add_region_field'),
    ]

    operations = [
        migrations.RunPython(safe_add_project_manager),
    ]
