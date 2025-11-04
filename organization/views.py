from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Organization, OrganizationMember
from .forms import OrganizationForm

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/create.html'
    success_url = reverse_lazy('organization_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Create owner membership
        OrganizationMember.objects.create(
            organization=self.object,
            user=self.request.user,
            role='owner'
        )
        return response

class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization/list.html'
    context_object_name = 'organizations'
    
    def get_queryset(self):
        # Show organizations where user is creator or member
        return Organization.objects.filter(
            Q(created_by=self.request.user) |
            Q(members__user=self.request.user)
        ).distinct()

class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'organization/detail.html'
    context_object_name = 'organization'
    
    def get_queryset(self):
        return Organization.objects.filter(
            Q(created_by=self.request.user) |
            Q(members__user=self.request.user)
        ).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.created_by == self.request.user
        context['user_membership'] = OrganizationMember.objects.filter(
            organization=self.object, user=self.request.user
        ).first()
        return context

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/update.html'
    success_url = reverse_lazy('organization_list')
    
    def get_queryset(self):
        # Only owners can update organization
        return Organization.objects.filter(created_by=self.request.user)