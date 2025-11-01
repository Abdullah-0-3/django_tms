from django.contrib import admin
from .models import Task, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'task_stage', 'task_priority', 'created_by', 'created_at')
    list_filter = ('task_stage', 'task_priority', 'created_at')
    search_fields = ('title', 'created_by__username', 'project__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'created_by__username', 'task__title')
    readonly_fields = ('created_at', 'updated_at')
