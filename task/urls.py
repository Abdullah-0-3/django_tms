from django.urls import path
from . import views

urlpatterns = [
    # Task URLs
    path('', views.ListTask.as_view(), name='task_list'),
    path('create/', views.CreateTask.as_view(), name='task_create'),
    path('<int:pk>/', views.DetailTask.as_view(), name='task_detail'),
    path('<int:pk>/update/', views.UpdateTask.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.DeleteTask.as_view(), name='task_delete'),
    
    # Comment URLs
    path('comments/', views.ListComment.as_view(), name='comment_list'),
    path('comment/<int:pk>/', views.DetailComment.as_view(), name='comment_detail'),
    path('comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='comment_delete'),
    path('<int:task_id>/comment/create/', views.CreateComment.as_view(), name='comment_create'),
]