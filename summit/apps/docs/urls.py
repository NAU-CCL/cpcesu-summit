from config.links import url_wrapper

from . import vars

app_name = vars.app_name
app_regex = vars.app_regex


urlpatterns = [
    # Links

    # URLs
    url_wrapper(vars.AppLinks.doc_detail),
    url_wrapper(vars.AppLinks.all_docs),
    url_wrapper(vars.AppLinks.doc_add_edit),
]
