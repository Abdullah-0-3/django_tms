from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Organization
from .forms import OrganizationForm

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/create.html'
    success_url = reverse_lazy('organization_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

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