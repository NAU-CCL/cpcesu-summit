from django.forms import ModelForm, ChoiceField

from .models import Organization, UserProfile, UserGroup


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']


class GroupForm(ModelForm):

    class Meta:
        model = Organization
        fields = ['name', 'description', 'logo', 'type', 'contact']
