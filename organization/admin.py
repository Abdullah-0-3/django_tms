from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at', 'created_by')
    search_fields = ('name', 'description', 'created_by__username')
    list_filter = ('created_at', 'updated_at')
