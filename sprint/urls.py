from django.urls import path
from . import views

urlpatterns = [
    # Organization/Project/Sprint hierarchy URLs
    path('<int:org_id>/project/<int:project_id>/sprint/', views.ListSprint.as_view(), name='org_project_sprint_list'),
    path('<int:org_id>/project/<int:project_id>/sprint/create/', views.CreateSprint.as_view(), name='org_project_sprint_create'),
    path('<int:org_id>/project/<int:project_id>/sprint/<int:pk>/', views.DetailSprint.as_view(), name='org_project_sprint_detail'),
    path('<int:org_id>/project/<int:project_id>/sprint/<int:pk>/update/', views.UpdateSprint.as_view(), name='org_project_sprint_update'),
    path('<int:org_id>/project/<int:project_id>/sprint/<int:pk>/delete/', views.DeleteSprint.as_view(), name='org_project_sprint_delete'),
]