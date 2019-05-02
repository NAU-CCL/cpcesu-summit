from config.links import app_link, url_wrapper

from . import vars


app_name = vars.app_name
app_regex = vars.app_regex

urlpatterns = [
    app_link(vars.AppLinks.index),
    app_link(vars.AppLinks.about)
]

# Static Links
app_link(vars.AppLinks.contact, True)
app_link(vars.AppLinks.admin_site, True)
