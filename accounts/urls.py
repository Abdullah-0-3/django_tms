from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.LogoutView.as_view(next_page='/'), name='logout')
]