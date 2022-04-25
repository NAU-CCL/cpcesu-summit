# Secondary URLs loaded in at the end for better nav bar

from django.apps import AppConfig
from config.links import app_link, url_wrapper
from summit.libs.auth.views import add_users, deactivate_user, delete_user

from . import vars

app_name = vars.app_name
app_regex = vars.app_regex

urlpatterns = [
    url_wrapper(vars.AppLinks.logged_out),
    url_wrapper(vars.AppLinks.edit_contact),
    url_wrapper(vars.AppLinks.edit_my_contact),
    url_wrapper(vars.AppLinks.view_my_contact),
    url_wrapper(vars.AppLinks.view_contact),

    app_link(vars.AppLinks.cesu_selector),
    app_link(vars.AppLinks.all_contacts),
    app_link(vars.AppLinks.all_organizations),
    app_link(vars.AppLinks.all_users),
    app_link(vars.AppLinks.create_contact),
    app_link(vars.AppLinks.create_organization),
    app_link(vars.AppLinks.create_user),
    app_link(vars.AppLinks.edit_user),
    app_link(vars.AppLinks.manage_my_organization),

    url_wrapper(vars.AppLinks.manage_organization),
    url_wrapper(vars.AppLinks.edit_organization),
    url_wrapper(vars.AppLinks.create_contact_in_group),
    url_wrapper(vars.AppLinks.info_display),
    url_wrapper(vars.AppLinks.org_info),
    url_wrapper(vars.AppLinks.user_info_display),
    url_wrapper(vars.AppLinks.deactivate_user),
    url_wrapper(vars.AppLinks.delete_user),
    url_wrapper(vars.AppLinks.add_users)
]
