from django.urls import path
from . import views

urlpatterns = [
    # Task Section with filters
    path('<int:org_id>/project/<int:project_id>/tasks/', views.TaskSection.as_view(), name='org_project_tasks'),
    path('<int:org_id>/project/<int:project_id>/task/create/', views.CreateTask.as_view(), name='org_project_task_create'),
    path('<int:org_id>/project/<int:project_id>/task/<int:pk>/', views.DetailTask.as_view(), name='org_project_task_detail'),
    path('<int:org_id>/project/<int:project_id>/task/<int:pk>/update/', views.UpdateTask.as_view(), name='org_project_task_update'),
    path('<int:org_id>/project/<int:project_id>/task/<int:pk>/delete/', views.DeleteTask.as_view(), name='org_project_task_delete'),
    
    # Task Comments
    path('<int:org_id>/project/<int:project_id>/task/<int:task_id>/comment/create/', views.CreateComment.as_view(), name='org_project_task_comment_create'),
    path('<int:org_id>/project/<int:project_id>/task/<int:task_id>/comment/<int:pk>/', views.DetailComment.as_view(), name='org_project_task_comment_detail'),
    path('<int:org_id>/project/<int:project_id>/task/<int:task_id>/comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='org_project_task_comment_delete'),
]