from django.urls import path
from . import views

urlpatterns = [
    path('<int:org_id>/invite/', views.invite_user, name='invite_user'),
    path('<int:org_id>/members/', views.organization_members, name='organization_members'),
    path('invitation/<uuid:invitation_id>/accept/', views.accept_invitation, name='accept_invitation'),
    path('invitation/<uuid:invitation_id>/decline/', views.decline_invitation, name='decline_invitation'),
]