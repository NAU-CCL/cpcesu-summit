from django import forms

from .models import CESURole, Organization, UserProfile, UserGroup, User, CESU


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'address': forms.TextInput(attrs={'placeholder': 'City, State, Zip'}),
            'cesu': forms.TextInput(),
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'description', 'logo', 'type', 'contact', 'city', 'state']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'user_cesus']
        widgets = {
            
        }
    user_cesus = forms.ModelMultipleChoiceField(
            queryset=CESU.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )

class RoleForm(forms.ModelForm):
    class Meta:
        model = CESURole
        fields = ['role']
        widgets = {
            
        }
        