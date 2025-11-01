from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm
from organization.models import Organization

class ProjectList(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_create.html'
    success_url = reverse_lazy('project_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        # Check if creating from organization page
        if 'org_id' in self.kwargs:
            kwargs['hide_organization'] = True
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'org_id' in self.kwargs:
            context['organization'] = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # If creating from organization page, set the organization
        if 'org_id' in self.kwargs:
            organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
            form.instance.organization = organization
            self.success_url = reverse_lazy('organization_detail', kwargs={'pk': organization.pk})
        return super().form_valid(form)

class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'project'
    
    def get_object(self):
        org = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        return get_object_or_404(Project, pk=self.kwargs['pk'], organization=org, created_by=self.request.user)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'
    
    def get_object(self):
        org = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        return get_object_or_404(Project, pk=self.kwargs['pk'], organization=org, created_by=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'org_id': self.kwargs['org_id'], 'pk': self.object.pk})

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/project_delete.html'
    
    def get_object(self):
        org = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        return get_object_or_404(Project, pk=self.kwargs['pk'], organization=org, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('organization_detail', kwargs={'pk': self.kwargs['org_id']})
