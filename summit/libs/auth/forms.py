from django import forms

from .models import Organization, UserProfile, UserGroup


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'address': forms.TextInput(attrs={'placeholder': 'City, State, Zip'})
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'description', 'logo', 'type', 'contact']
