from django.urls import path
from .views import ProjectList, ProjectCreate, ProjectDetail, ProjectUpdate, ProjectDelete

urlpatterns = [
    path('project/', ProjectList.as_view(), name='project_list'),
    path('project/create/', ProjectCreate.as_view(), name='project_create'),
    path('<int:org_id>/project/create/', ProjectCreate.as_view(), name='project_create_for_org'),
    path('<int:org_id>/project/<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('<int:org_id>/project/<int:pk>/update/', ProjectUpdate.as_view(), name='project_update'),
    path('<int:org_id>/project/<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete'),
]