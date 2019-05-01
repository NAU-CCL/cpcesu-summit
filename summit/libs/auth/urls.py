# Primary URLs loaded in to the nav bar first
from config.links import url_wrapper

from . import vars

app_name = vars.app_name
app_regex = vars.app_regex
urlpatterns = [
    url_wrapper(vars.AppLinks.logged_out),
    url_wrapper(vars.AppLinks.edit_contact),
    url_wrapper(vars.AppLinks.edit_my_contact),
    url_wrapper(vars.AppLinks.view_my_contact),
    url_wrapper(vars.AppLinks.view_contact)
]
