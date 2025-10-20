# projects/migrations/0004_add_robust_fields.py
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_add_region_field'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Add project_manager field (essential for accountability)
        migrations.AddField(
            model_name='project',
            name='project_manager',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='project_managed_projects',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Project Manager',
                help_text='Primary accountable person for project delivery'
            ),
        ),
        # Add risk_notes field (essential for risk management)
        migrations.AddField(
            model_name='project',
            name='risk_notes',
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name='Risk Assessment Notes',
                help_text='Detailed risk analysis, mitigation strategies, and contingency plans'
            ),
        ),
    ]
