# Enable delete in projects admin
with open('projects/admin.py', 'w') as f:
    f.write('''
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'budget', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    actions = ['delete_selected']  # ENABLE DELETE
    
    # Soft delete option
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
''')

print(' Enabled delete in projects admin')
