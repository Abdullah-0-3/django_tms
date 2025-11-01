from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task, Comment
from .forms import TaskForm, CommentForm
from project.models import Project
from organization.models import Organization
from sprint.models import Sprint

class TaskSection(LoginRequiredMixin, ListView):
    template_name = 'task/section.html'
    model = Task
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        
        filter_type = self.request.GET.get('filter', 'all')
        stage_filter = self.request.GET.get('stage', 'all')
        
        # Base queryset
        queryset = Task.objects.filter(project=project, created_by=self.request.user)
        
        # Apply sprint/regular filter
        if filter_type == 'sprint':
            queryset = queryset.filter(sprint__isnull=False)
        elif filter_type == 'regular':
            queryset = queryset.filter(sprint__isnull=True)
        
        # Apply stage filter
        if stage_filter in ['to do', 'in progress', 'done']:
            queryset = queryset.filter(task_stage=stage_filter)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        
        context['organization'] = organization
        context['project'] = project
        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['current_stage'] = self.request.GET.get('stage', 'all')
        
        # Task counts
        all_tasks = Task.objects.filter(project=project, created_by=self.request.user)
        context['all_count'] = all_tasks.count()
        context['sprint_count'] = all_tasks.filter(sprint__isnull=False).count()
        context['regular_count'] = all_tasks.filter(sprint__isnull=True).count()
        
        # Stage counts
        context['todo_count'] = all_tasks.filter(task_stage='to do').count()
        context['inprogress_count'] = all_tasks.filter(task_stage='in progress').count()
        context['done_count'] = all_tasks.filter(task_stage='done').count()
        
        return context

class DetailTask(LoginRequiredMixin, DetailView):
    template_name = 'task/detail.html'
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(task=self.object)
        context['organization'] = self.object.project.organization
        context['project'] = self.object.project
        return context

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        return Task.objects.filter(project=project, created_by=self.request.user)

class CreateTask(LoginRequiredMixin, CreateView):
    template_name = 'task/create.html'
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['hide_project'] = True
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        kwargs['project'] = project
        return kwargs
    
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
        # Sprint is handled by the form, no need to override it
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('org_project_tasks', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id']})

class UpdateTask(LoginRequiredMixin, UpdateView):
    template_name = 'task/update.html'
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        kwargs['project'] = project
        return kwargs

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        return Task.objects.filter(project=project, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_task_detail', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'pk': self.object.pk})

class DeleteTask(LoginRequiredMixin, DeleteView):
    template_name = 'task/delete.html'
    model = Task

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        return Task.objects.filter(project=project, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_tasks', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id']})


# Comments Secitons

class CreateComment(LoginRequiredMixin, CreateView):
    template_name = 'task/comment_create.html'
    model = Comment
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], project=project)
        context['organization'] = organization
        context['project'] = project
        context['task'] = task
        return context
    
    def form_valid(self, form):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], project=project)
        form.instance.task = task
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('org_project_task_detail', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'pk': self.kwargs['task_id']})

class ListComment(LoginRequiredMixin, ListView):
    template_name = 'task/comment_list.html'
    model = Comment
    context_object_name = 'comments'
    paginate_by = 10
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], project=project)
        return Comment.objects.filter(task=task).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], project=project)
        context['organization'] = organization
        context['project'] = project
        context['task'] = task
        return context

class DetailComment(LoginRequiredMixin, DetailView):
    template_name = 'task/comment_detail.html'
    model = Comment
    context_object_name = 'comment'
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], project=project)
        return Comment.objects.filter(task=task)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        context['organization'] = organization
        context['project'] = project
        context['task'] = self.object.task
        return context

class DeleteComment(LoginRequiredMixin, DeleteView):
    template_name = 'task/comment_delete.html'
    model = Comment
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], project=project)
        return Comment.objects.filter(task=task, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_task_detail', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'pk': self.object.task.pk})


# Sprint Task Views

class ListSprintTask(LoginRequiredMixin, ListView):
    template_name = 'task/sprint_task_list.html'
    model = Task
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        return Task.objects.filter(sprint=sprint, created_by=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        
        context['organization'] = organization
        context['project'] = project
        context['sprint'] = sprint
        return context

class CreateSprintTask(LoginRequiredMixin, CreateView):
    template_name = 'task/sprint_task_create.html'
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['hide_project'] = True
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        kwargs['project'] = project
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        context['organization'] = organization
        context['project'] = project
        context['sprint'] = sprint
        return context

    def form_valid(self, form):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        form.instance.project = project
        form.instance.sprint = sprint
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_task_list', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'sprint_id': self.kwargs['sprint_id']})

class DetailSprintTask(LoginRequiredMixin, DetailView):
    template_name = 'task/sprint_task_detail.html'
    model = Task
    context_object_name = 'task'

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        return Task.objects.filter(sprint=sprint, created_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(task=self.object)
        context['organization'] = self.object.project.organization
        context['project'] = self.object.project
        context['sprint'] = self.object.sprint
        return context

class UpdateSprintTask(LoginRequiredMixin, UpdateView):
    template_name = 'task/sprint_task_update.html'
    model = Task
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        kwargs['project'] = project
        return kwargs

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        return Task.objects.filter(sprint=sprint, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_task_detail', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'sprint_id': self.kwargs['sprint_id'], 'pk': self.object.pk})

class DeleteSprintTask(LoginRequiredMixin, DeleteView):
    template_name = 'task/sprint_task_delete.html'
    model = Task

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        return Task.objects.filter(sprint=sprint, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_task_list', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'sprint_id': self.kwargs['sprint_id']})

# Sprint Task Comment Views

class CreateSprintTaskComment(LoginRequiredMixin, CreateView):
    template_name = 'task/sprint_task_comment_create.html'
    model = Comment
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], sprint=sprint)
        context['organization'] = organization
        context['project'] = project
        context['sprint'] = sprint
        context['task'] = task
        return context
    
    def form_valid(self, form):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], sprint=sprint)
        form.instance.task = task
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_task_detail', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'sprint_id': self.kwargs['sprint_id'], 'pk': self.kwargs['task_id']})

class DetailSprintTaskComment(LoginRequiredMixin, DetailView):
    template_name = 'task/sprint_task_comment_detail.html'
    model = Comment
    context_object_name = 'comment'
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], sprint=sprint)
        return Comment.objects.filter(task=task)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        context['organization'] = organization
        context['project'] = project
        context['sprint'] = sprint
        context['task'] = self.object.task
        return context

class DeleteSprintTaskComment(LoginRequiredMixin, DeleteView):
    template_name = 'task/sprint_task_comment_delete.html'
    model = Comment
    
    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs['org_id'], created_by=self.request.user)
        project = get_object_or_404(Project, pk=self.kwargs['project_id'], organization=organization, created_by=self.request.user)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['sprint_id'], project=project, created_by=self.request.user)
        task = get_object_or_404(Task, pk=self.kwargs['task_id'], sprint=sprint)
        return Comment.objects.filter(task=task, created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('org_project_sprint_task_detail', kwargs={'org_id': self.kwargs['org_id'], 'project_id': self.kwargs['project_id'], 'sprint_id': self.kwargs['sprint_id'], 'pk': self.object.task.pk})
