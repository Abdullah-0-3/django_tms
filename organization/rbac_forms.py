from django import forms
from django.contrib.auth import get_user_model
from .models import OrganizationRole, Permission, RolePermission

User = get_user_model()

class InviteUserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'})
    )
    role = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a role"
    )
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['role'].queryset = organization.roles.all()

class RoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = OrganizationRole
        fields = ['name', 'role_type', 'description', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if organization:
            self.fields['permissions'].queryset = organization.permissions.all()
    
    def save(self, commit=True):
        role = super().save(commit)
        if commit:
            # Clear existing permissions
            RolePermission.objects.filter(role=role).delete()
            # Add selected permissions
            for permission in self.cleaned_data['permissions']:
                RolePermission.objects.create(role=role, permission=permission)
        return role

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'codename', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'codename': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }