from django.db import models
from django.contrib.auth import get_user_model
from .models import Organization

User = get_user_model()

class OrganizationRole(models.Model):
    ROLE_CHOICES = [
        ('lead', 'Organization Lead'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
        ('custom', 'Custom Role'),
    ]
    
    name = models.CharField(max_length=100)
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='roles')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_roles')
    
    class Meta:
        unique_together = ['name', 'organization']
    
    def __str__(self):
        return f"{self.name} - {self.organization.name}"

class Permission(models.Model):
    PERMISSION_TYPES = [
        ('organization.view', 'View Organization'),
        ('organization.edit', 'Edit Organization'),
        ('organization.delete', 'Delete Organization'),
        ('organization.invite', 'Invite Users'),
        ('project.view', 'View Projects'),
        ('project.create', 'Create Projects'),
        ('project.edit', 'Edit Projects'),
        ('project.delete', 'Delete Projects'),
        ('task.view', 'View Tasks'),
        ('task.create', 'Create Tasks'),
        ('task.edit', 'Edit Tasks'),
        ('task.delete', 'Delete Tasks'),
        ('sprint.view', 'View Sprints'),
        ('sprint.create', 'Create Sprints'),
        ('sprint.edit', 'Edit Sprints'),
        ('sprint.delete', 'Delete Sprints'),
    ]
    
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, choices=PERMISSION_TYPES)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_permissions')
    
    class Meta:
        unique_together = ['codename', 'organization']
    
    def __str__(self):
        return f"{self.name} ({self.get_codename_display()})"

class RolePermission(models.Model):
    role = models.ForeignKey(OrganizationRole, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='roles')
    
    class Meta:
        unique_together = ['role', 'permission']

class OrganizationMembership(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_memberships')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    role = models.ForeignKey(OrganizationRole, on_delete=models.CASCADE, related_name='memberships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'organization']
    
    def __str__(self):
        return f"{self.user.username} - {self.organization.name} ({self.role.name})"

class OrganizationInvitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]
    
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invitations')
    role = models.ForeignKey(OrganizationRole, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_invitations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Invitation to {self.email} for {self.organization.name}"