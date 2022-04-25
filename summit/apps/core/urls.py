from config.links import app_link, url_wrapper

from . import vars


app_name = vars.app_name
app_regex = vars.app_regex

urlpatterns = [
    #url_wrapper(vars.AppLinks.index),
    app_link(vars.AppLinks.about),
    app_link(vars.AppLinks.tiles),
]

# Static Links
app_link(vars.AppLinks.contact, True)
