from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta
from .models import Organization
from .rbac_models import OrganizationRole, Permission, RolePermission, OrganizationMembership, OrganizationInvitation
from .forms import InviteUserForm, RoleForm, PermissionForm

User = get_user_model()

class OrganizationMembersView(LoginRequiredMixin, ListView):
    template_name = 'organization/members.html'
    context_object_name = 'memberships'
    
    def get_queryset(self):
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'], created_by=self.request.user)
        return self.organization.memberships.filter(status='active')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        context['pending_invitations'] = self.organization.invitations.filter(status='pending')
        return context

class InviteUserView(LoginRequiredMixin, CreateView):
    form_class = InviteUserForm
    template_name = 'organization/invite_user.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'], created_by=self.request.user)
        kwargs['organization'] = self.organization
        return kwargs
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        role = form.cleaned_data['role']
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
            # Check if already a member
            if OrganizationMembership.objects.filter(user=user, organization=self.organization).exists():
                messages.error(self.request, f'{email} is already a member of this organization.')
                return self.form_invalid(form)
            
            # Create membership directly
            OrganizationMembership.objects.create(
                user=user,
                organization=self.organization,
                role=role,
                invited_by=self.request.user
            )
            messages.success(self.request, f'{email} has been added to the organization.')
        except User.DoesNotExist:
            # Create invitation
            token = get_random_string(50)
            expires_at = timezone.now() + timedelta(days=7)
            
            OrganizationInvitation.objects.create(
                email=email,
                organization=self.organization,
                role=role,
                invited_by=self.request.user,
                token=token,
                expires_at=expires_at
            )
            messages.success(self.request, f'Invitation sent to {email}.')
        
        return redirect('organization_members', pk=self.organization.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context

class OrganizationRolesView(LoginRequiredMixin, ListView):
    template_name = 'organization/roles.html'
    context_object_name = 'roles'
    
    def get_queryset(self):
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'], created_by=self.request.user)
        return self.organization.roles.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context

class CreateRoleView(LoginRequiredMixin, CreateView):
    model = OrganizationRole
    form_class = RoleForm
    template_name = 'organization/create_role.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'], created_by=self.request.user)
        kwargs['organization'] = self.organization
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.organization
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('organization_roles', kwargs={'pk': self.organization.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context

class OrganizationPermissionsView(LoginRequiredMixin, ListView):
    template_name = 'organization/permissions.html'
    context_object_name = 'permissions'
    
    def get_queryset(self):
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'], created_by=self.request.user)
        return self.organization.permissions.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context

class CreatePermissionView(LoginRequiredMixin, CreateView):
    model = Permission
    form_class = PermissionForm
    template_name = 'organization/create_permission.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.organization = get_object_or_404(Organization, pk=self.kwargs['pk'], created_by=self.request.user)
        return kwargs
    
    def form_valid(self, form):
        form.instance.organization = self.organization
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('organization_permissions', kwargs={'pk': self.organization.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.organization
        return context