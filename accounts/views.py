from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'You have been successfully logged in!')
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})