from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from organization.models import Organization
from .models import Invitation, OrganizationMember
from .forms import InvitationForm

User = get_user_model()

@login_required
def invite_user(request, org_id):
    organization = get_object_or_404(Organization, id=org_id, created_by=request.user)
    
    if request.method == 'POST':
        form = InvitationForm(request.POST, organization=organization)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.organization = organization
            invitation.invited_by = request.user
            invitation.save()
            messages.success(request, f'Invitation sent to {invitation.email}')
            return redirect('organization_detail', pk=org_id)
    else:
        form = InvitationForm(organization=organization)
    
    return render(request, 'organization/rbac/invite.html', {
        'form': form,
        'organization': organization
    })

@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, status='pending')
    
    # Check if the current user's email matches the invitation
    if request.user.email != invitation.email:
        messages.error(request, 'This invitation is not for your email address.')
        return redirect('organization_list')
    
    # Create organization membership
    OrganizationMember.objects.create(
        organization=invitation.organization,
        user=request.user,
        role=invitation.role
    )
    
    # Update invitation status
    invitation.status = 'accepted'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    messages.success(request, f'You have joined {invitation.organization.name}!')
    return redirect('organization_detail', pk=invitation.organization.id)

@login_required
def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, status='pending')
    
    if request.user.email != invitation.email:
        messages.error(request, 'This invitation is not for your email address.')
        return redirect('organization_list')
    
    invitation.status = 'declined'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    messages.info(request, f'You have declined the invitation to {invitation.organization.name}.')
    return redirect('organization_list')

@login_required
def organization_members(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    
    # Check if user has access to this organization
    if not (organization.created_by == request.user or 
            OrganizationMember.objects.filter(organization=organization, user=request.user).exists()):
        messages.error(request, 'You do not have access to this organization.')
        return redirect('organization_list')
    
    members = OrganizationMember.objects.filter(organization=organization).select_related('user')
    pending_invitations = Invitation.objects.filter(organization=organization, status='pending')
    
    return render(request, 'organization/rbac/members.html', {
        'organization': organization,
        'members': members,
        'pending_invitations': pending_invitations,
        'is_owner': organization.created_by == request.user
    })