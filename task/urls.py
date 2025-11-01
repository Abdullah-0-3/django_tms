from django.urls import path
from . import views

urlpatterns = [
    # Organization/Project/Task hierarchy URLs
    path('<int:org_id>/project/<int:project_id>/task/', views.ListTask.as_view(), name='org_project_task_list'),
    path('<int:org_id>/project/<int:project_id>/task/create/', views.CreateTask.as_view(), name='org_project_task_create'),
    path('<int:org_id>/project/<int:project_id>/task/<int:pk>/', views.DetailTask.as_view(), name='org_project_task_detail'),
    path('<int:org_id>/project/<int:project_id>/task/<int:pk>/update/', views.UpdateTask.as_view(), name='org_project_task_update'),
    path('<int:org_id>/project/<int:project_id>/task/<int:pk>/delete/', views.DeleteTask.as_view(), name='org_project_task_delete'),
    
    # Comment URLs
    path('<int:org_id>/project/<int:project_id>/task/<int:task_id>/comment/', views.ListComment.as_view(), name='org_project_task_comment_list'),
    path('<int:org_id>/project/<int:project_id>/task/<int:task_id>/comment/create/', views.CreateComment.as_view(), name='org_project_task_comment_create'),
    path('<int:org_id>/project/<int:project_id>/task/<int:task_id>/comment/<int:pk>/', views.DetailComment.as_view(), name='org_project_task_comment_detail'),
    path('<int:org_id>/project/<int:project_id>/task/<int:task_id>/comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='org_project_task_comment_delete'),
]