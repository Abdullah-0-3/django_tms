from django.db import models
from project.models import Project

class Task(models.Model):

    TASK_PRIORITY = (
        ("h", "High"),
        ("m", "Medium"),
        ("l", "Low"),
    )

    TASK_STAGE = (
        ('to do', "To Do"),
        ('in progress', 'In Progress'),
        ('done', 'Done'),
    )

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks'
    )
    sprint = models.ForeignKey(
        'sprint.Sprint', on_delete=models.CASCADE, null=True, blank=True, related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    task_stage = models.CharField(max_length=20, choices=TASK_STAGE, default='to do')
    task_priority = models.CharField(max_length=1, choices=TASK_PRIORITY, default='m')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', related_name='created_tasks', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} - {self.project.title}"

class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', related_name='created_comments', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} - {self.task.title}"
