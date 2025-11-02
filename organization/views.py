from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Organization
from .forms import OrganizationForm
from .rbac_models import OrganizationRole, Permission, OrganizationMembership

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/create.html'
    success_url = reverse_lazy('organization_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Create default roles for the organization
        self.create_default_roles()
        
        # Add creator as Lead
        lead_role = OrganizationRole.objects.get(organization=self.object, role_type='lead')
        OrganizationMembership.objects.create(
            user=self.request.user,
            organization=self.object,
            role=lead_role,
            invited_by=self.request.user
        )
        
        messages.success(self.request, f'Organization "{self.object.name}" created successfully. You are now the Lead.')
        return response
    
    def create_default_roles(self):
        """Create default roles and permissions for new organization"""
        # Create default permissions
        default_permissions = [
            ('View Organization', 'organization.view'),
            ('Edit Organization', 'organization.edit'),
            ('Delete Organization', 'organization.delete'),
            ('Invite Users', 'organization.invite'),
            ('View Projects', 'project.view'),
            ('Create Projects', 'project.create'),
            ('Edit Projects', 'project.edit'),
            ('Delete Projects', 'project.delete'),
            ('View Tasks', 'task.view'),
            ('Create Tasks', 'task.create'),
            ('Edit Tasks', 'task.edit'),
            ('Delete Tasks', 'task.delete'),
            ('View Sprints', 'sprint.view'),
            ('Create Sprints', 'sprint.create'),
            ('Edit Sprints', 'sprint.edit'),
            ('Delete Sprints', 'sprint.delete'),
        ]
        
        for name, codename in default_permissions:
            Permission.objects.create(
                name=name,
                codename=codename,
                organization=self.object,
                created_by=self.request.user
            )
        
        # Create default roles
        OrganizationRole.objects.create(
            name='Lead',
            role_type='lead',
            organization=self.object,
            description='Organization leader with full access',
            created_by=self.request.user
        )
        
        OrganizationRole.objects.create(
            name='Admin',
            role_type='admin',
            organization=self.object,
            description='Administrator with management access',
            created_by=self.request.user
        )
        
        OrganizationRole.objects.create(
            name='Member',
            role_type='member',
            organization=self.object,
            description='Regular member with basic access',
            created_by=self.request.user
        )
        
        OrganizationRole.objects.create(
            name='Viewer',
            role_type='viewer',
            organization=self.object,
            description='Read-only access',
            created_by=self.request.user
        )

class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization/list.html'
    context_object_name = 'organizations'
    
    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)

class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'organization/detail.html'
    context_object_name = 'organization'
    
    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/update.html'
    success_url = reverse_lazy('organization_list')
    
    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)