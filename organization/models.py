from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Organization(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='organizations'
    )

    def __str__(self):
        return self.name
    
    def get_lead(self):
        """Get the organization lead"""
        return self.created_by
    
    def has_permission(self, user, permission_codename):
        """Check if user has specific permission in this organization"""
        if user == self.created_by:  # Lead has all permissions
            return True
        
        try:
            membership = self.memberships.get(user=user, status='active')
            return membership.role.permissions.filter(
                permission__codename=permission_codename
            ).exists()
        except:
            return False

# Import RBAC models
from .rbac_models import *
