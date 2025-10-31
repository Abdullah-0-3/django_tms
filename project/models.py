from django.db import models
from organization.models import Organization

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='created_projects'
    )

    def __str__(self):
        return f"{self.title} - {self.organization.name}"
