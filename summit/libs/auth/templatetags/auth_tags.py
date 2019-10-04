from django import template
from django.contrib.auth.forms import PasswordChangeForm

register = template.Library()


@register.inclusion_tag('registration/partials/change_password.html')
def change_password_partial():
    return {'form': PasswordChangeForm()}


@register.inclusion_tag('registration/edit_profile.html', takes_context=True)
def edit_profile_partial(context):
    return context
