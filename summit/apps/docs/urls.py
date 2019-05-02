from config.links import app_link, url_wrapper

from . import vars

app_name = vars.app_name
app_regex = vars.app_regex

urlpatterns = [
    # Links
    app_link(vars.AppLinks.doc_detail),
    app_link(vars.AppLinks.all_docs),
    app_link(vars.AppLinks.doc_add_edit),

    # URLs

]
