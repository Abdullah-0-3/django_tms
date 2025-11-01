"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('organization/', include('organization.urls')),
    path('organization/', include('project.urls')),
    path('organization/', include('sprint.urls')),
    path('organization/', include('task.urls')),
]

# Error handlers
handler400 = 'core.views.handler400'
handler401 = 'core.views.handler401'
handler403 = 'core.views.handler403'
handler404 = 'core.views.handler404'
handler405 = 'core.views.handler405'
handler429 = 'core.views.handler429'
handler500 = 'core.views.handler500'
handler502 = 'core.views.handler502'
handler503 = 'core.views.handler503'
handler504 = 'core.views.handler504'
