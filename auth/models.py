from django.db import models
from organization.models import Organization
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    organization = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.SET_NULL, related_name='users'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        org_name = self.organization.name if self.organization else "No Organization"
        return f"{self.username} - {org_name}"

