from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                raise PermissionDenied("You don't have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def system_admin_required(view_func):
    return role_required(['system_admin'])(view_func)

def project_manager_required(view_func):
    return role_required(['system_admin', 'project_manager'])(view_func)

def finance_officer_required(view_func):
    return role_required(['system_admin', 'finance_officer'])(view_func)