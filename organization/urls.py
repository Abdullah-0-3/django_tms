from django.urls import path
from organization import views

urlpatterns = [
    path('create/', views.OrganizationCreateView.as_view(), name='create_organization'),
    path('<int:pk>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
    path('<int:pk>/update/', views.OrganizationUpdateView.as_view(), name='organization_update'),
    path('', views.OrganizationListView.as_view(), name='organization_list'),
]