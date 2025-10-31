from django.urls import path
from organization import views

urlpatterns = [
    path('create/', views.OrganizationCreateView.as_view(), name='create_organization'),
    path('', views.OrganizationListView.as_view(), name='organization_list'),
]