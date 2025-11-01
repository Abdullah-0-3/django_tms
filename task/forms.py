from django import forms
from .models import Task, Comment
from project.models import Project
from sprint.models import Sprint

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'sprint', 'title', 'description', 'task_stage', 'task_priority']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'sprint': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'task_stage': forms.Select(attrs={'class': 'form-control'}),
            'task_priority': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        project = kwargs.pop('project', None)
        hide_project = kwargs.pop('hide_project', False)
        super().__init__(*args, **kwargs)
        
        # Make sprint field optional
        self.fields['sprint'].required = False
        self.fields['sprint'].empty_label = "No Sprint (Regular Task)"
        
        if user:
            self.fields['project'].queryset = Project.objects.filter(created_by=user)
            
        # Set sprint queryset based on project
        if project:
            self.fields['sprint'].queryset = Sprint.objects.filter(project=project, created_by=user)
        elif user:
            self.fields['sprint'].queryset = Sprint.objects.filter(created_by=user)
            
        if hide_project:
            del self.fields['project']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }