from django.urls import path
from .views import ProjectList, ProjectCreate, ProjectDetail, ProjectUpdate, ProjectDelete

urlpatterns = [
    path('', ProjectList.as_view(), name='project_list'),
    path('create/', ProjectCreate.as_view(), name='project_create'),
    path('organization/<int:org_id>/create/', ProjectCreate.as_view(), name='project_create_for_org'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('<int:pk>/update/', ProjectUpdate.as_view(), name='project_update'),
    path('<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete'),
]