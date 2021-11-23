from django.forms import ModelForm, ChoiceField

from .models import Organization, UserProfile, UserGroup


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']


class GroupForm(ModelForm):
    group_type = ChoiceField(choices=(
        (1, "CES Unit"),
        (2, "Federal Agency"),
        (3, "Partner")
    ))

    class Meta:
        model = Organization
        fields = ['name', 'description', 'logo', 'contact']
