from django import forms
from .models import Invitation, OrganizationMember

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email', 'role']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if self.organization:
            # Check if user is already a member
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                if OrganizationMember.objects.filter(organization=self.organization, user=user).exists():
                    raise forms.ValidationError("This user is already a member of the organization.")
            except User.DoesNotExist:
                pass
            
            # Check if there's already a pending invitation
            if Invitation.objects.filter(organization=self.organization, email=email, status='pending').exists():
                raise forms.ValidationError("An invitation has already been sent to this email.")
        
        return email