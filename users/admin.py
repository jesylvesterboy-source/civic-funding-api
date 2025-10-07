from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Displayed columns in user list
    list_display = (
        'username', 'email', 'role', 'phone_number', 
        'organization', 'is_verified', 'is_staff', 'is_active', 'date_joined'
    )

    # Filters on the right panel
    list_filter = (
        'role', 'is_verified', 'is_staff', 'is_active', 'is_superuser', 'date_joined'
    )

    # Search box fields
    search_fields = ('username', 'email', 'phone_number', 'organization')

    # Read-only fields (optional)
    readonly_fields = ('date_joined', 'last_login')

    # Fieldsets for viewing and editing users
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'role', 
                'phone_number', 
                'organization', 
                'is_verified',
            )
        }),
    )

    # Fieldsets when adding new users from the admin panel
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            # Note: We must include the fields that UserAdmin expects for 'Add User' but
            # since they are custom fields, they are added here.
            'fields': (
                'role',
                'phone_number',
                'organization',
                'is_verified',
            )
        }),
    )

    ordering = ('-date_joined',)