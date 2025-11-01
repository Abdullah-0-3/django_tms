from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Sprint
from .forms import SprintForm
from project.models import Project
from organization.models import Organization

class ListSprint(LoginRequiredMixin, ListView):
    template_name = 'sprint/list.html'
    model = Sprint
    context_object_name = 'sprints'
    paginate_by = 10
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        return Sprint.objects.filter(project=project, created_by=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        context['organization'] = organization
        context['project'] = project
        return context

class DetailSprint(LoginRequiredMixin, DetailView):
    template_name = 'sprint/detail.html'
    model = Sprint
    context_object_name = 'sprint'

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        return Sprint.objects.filter(project=project, created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.object.project.organization
        context['project'] = self.object.project
        context['sprint_tasks'] = self.object.tasks.filter(created_by=self.request.user)
        return context

class CreateSprint(LoginRequiredMixin, CreateView):
    template_name = 'sprint/create.html'
    model = Sprint
    form_class = SprintForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        context['organization'] = organization
        context['project'] = project
        return context

    def form_valid(self, form):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        form.instance.project = project
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_list', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id']})

class UpdateSprint(LoginRequiredMixin, UpdateView):
    template_name = 'sprint/update.html'
    model = Sprint
    form_class = SprintForm

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        return Sprint.objects.filter(project=project, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_detail', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'pk': self.object.pk})

class DeleteSprint(LoginRequiredMixin, DeleteView):
    template_name = 'sprint/delete.html'
    model = Sprint

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        return Sprint.objects.filter(project=project, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_list', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id']})