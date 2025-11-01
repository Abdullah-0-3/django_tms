from django.db import models
from project.models import Project

class Sprint(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='sprints'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_sprints')

    def __str__(self):
        return self.name
