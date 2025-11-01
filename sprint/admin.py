from django.contrib import admin
from sprint.models import Sprint

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'project')