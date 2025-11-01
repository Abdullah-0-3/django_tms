from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task, Comment
from .forms import TaskForm, CommentForm

class ListTask(LoginRequiredMixin, ListView):
    template_name = 'task/list.html'
    model = Task
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user).order_by('-created_at')

class DetailTask(LoginRequiredMixin, DetailView):
    template_name = 'task/detail.html'
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(task=self.object)
        return context

    def get_queryset(self):
            return Task.objects.filter(created_by=self.request.user)

class CreateTask(LoginRequiredMixin, CreateView):
    template_name = 'task/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class UpdateTask(LoginRequiredMixin, UpdateView):
    template_name = 'task/update.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

class DeleteTask(LoginRequiredMixin, DeleteView):
    template_name = 'task/delete.html'
    model = Task
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


# Comments Secitons

class CreateComment(LoginRequiredMixin, CreateView):
    template_name = 'task/comment_create.html'
    model = Comment
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['task_id'])
        return context
    
    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['task_id'])
        form.instance.task = task
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.kwargs['task_id']})

class ListComment(LoginRequiredMixin, ListView):
    template_name = 'task/comment_list.html'
    model = Comment
    context_object_name = 'comments'
    paginate_by = 10
    
    def get_queryset(self):
        return Comment.objects.filter(created_by=self.request.user).order_by('-created_at')

class DetailComment(LoginRequiredMixin, DetailView):
    template_name = 'task/comment_detail.html'
    model = Comment
    context_object_name = 'comment'
    
    def get_queryset(self):
        return Comment.objects.filter(created_by=self.request.user)

class DeleteComment(LoginRequiredMixin, DeleteView):
    template_name = 'task/comment_delete.html'
    model = Comment
    
    def get_queryset(self):
        return Comment.objects.filter(created_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.task.pk})
