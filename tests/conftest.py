import os
import django
import pytest
from django.conf import settings
from django.test import Client
from django.contrib.auth import get_user_model

# ---------------------------------------
# Django setup for pytest
# ---------------------------------------
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gates_tracker.settings')
    django.setup()

User = get_user_model()

# ---------------------------------------
# Global Fixtures
# ---------------------------------------

@pytest.fixture
def client():
    """Provide Django test client."""
    return Client()

@pytest.fixture
def admin_user(db):
    """Fixture for system admin user."""
    return User.objects.create_superuser(
        username='admin_user',
        email='admin@example.com',
        password='testpass123',
        role='system_admin'
    )

@pytest.fixture
def project_manager(db):
    """Fixture for project manager user."""
    return User.objects.create_user(
        username='pm_user',
        email='pm@example.com',
        password='testpass123',
        role='project_manager'
    )

@pytest.fixture
def finance_officer(db):
    """Fixture for finance officer user."""
    return User.objects.create_user(
        username='finance_user',
        email='finance@example.com',
        password='testpass123',
        role='finance_officer'
    )

@pytest.fixture
def field_officer(db):
    """Fixture for field officer user."""
    return User.objects.create_user(
        username='fo_user',
        email='fo@example.com',
        password='testpass123',
        role='field_officer'
    )