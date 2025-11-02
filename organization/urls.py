from django.urls import path
from organization import views
from organization.rbac_views import (
    OrganizationMembersView, InviteUserView, OrganizationRolesView, 
    CreateRoleView, OrganizationPermissionsView, CreatePermissionView
)

urlpatterns = [
    path('create/', views.OrganizationCreateView.as_view(), name='create_organization'),
    path('<int:pk>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('<int:pk>/update/', views.OrganizationUpdateView.as_view(), name='organization_update'),
    path('', views.OrganizationListView.as_view(), name='organization_list'),
    
    # RBAC URLs
    path('<int:pk>/members/', OrganizationMembersView.as_view(), name='organization_members'),
    path('<int:pk>/invite/', InviteUserView.as_view(), name='invite_user'),
    path('<int:pk>/roles/', OrganizationRolesView.as_view(), name='organization_roles'),
    path('<int:pk>/roles/create/', CreateRoleView.as_view(), name='create_role'),
    path('<int:pk>/permissions/', OrganizationPermissionsView.as_view(), name='organization_permissions'),
    path('<int:pk>/permissions/create/', CreatePermissionView.as_view(), name='create_permission'),
]