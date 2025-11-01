from django.urls import path
from .views import ProjectList, ProjectCreate, ProjectDetail, ProjectUpdate, ProjectDelete

urlpatterns = [
    path('<int:org_id>/project/', ProjectList.as_view(), name='org_project_list'),
    path('<int:org_id>/project/create/', ProjectCreate.as_view(), name='project_create_for_org'),
    path('<int:org_id>/project/<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('<int:org_id>/project/<int:pk>/update/', ProjectUpdate.as_view(), name='project_update'),
    path('<int:org_id>/project/<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete'),
]