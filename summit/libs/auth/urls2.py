# Secondary URLs loaded in at the end for better nav bar
from django.conf.urls import url

from config.links import link, get_name

from . import views


app_name = 'summit.libs.auth2'
app_regex = r'^accounts/'
urlpatterns = [
    link(r'^all_users/$', views.all_users, name=get_name(app_name, "All Groups and Users"), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
        'dropdown_name': 'Groups and Users'
    }),
    link(r'^create_group/$', views.create_group, name=get_name(app_name, "Create Group"), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
    }),
    link(r'^create_user/$', views.create_profile, name=get_name(app_name, "Create User"), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
    }),
    link(r'^manage_group/$', views.manage_group, name=get_name(app_name, "Manage My Group"), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
    }),

    url(r'^manage_group/(?P<group_id>[-\w]+)/$', views.manage_group, name='manage_group_other'),
    url(r'^create_user/(?P<group_id>[-\w]+)/$', views.create_profile, name='create_user_with_group')
]
