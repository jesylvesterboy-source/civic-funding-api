import pytest
from django.urls import reverse
from core.decorators import role_required

class TestRolePermissions:
    def test_role_required_decorator(self, project_manager):
        @role_required(['project_manager', 'system_admin'])
        def test_view(request):
            return "Success"
        
        # This should be tested with a mock request
        # In practice, you'd use Django's test client
        
    def test_user_permission_properties(self, project_manager, finance_officer):
        assert project_manager.can_manage_projects == True
        assert project_manager.can_manage_finances == False
        assert finance_officer.can_manage_finances == True