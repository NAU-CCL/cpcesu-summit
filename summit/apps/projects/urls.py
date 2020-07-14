from config.links import app_link, url_wrapper

from . import vars

app_name = vars.app_name
app_regex = vars.app_regex
urlpatterns = [
    # Project Links
    app_link(vars.AppLinks.project_dashboard),
    app_link(vars.AppLinks.all_projects),
    app_link(vars.AppLinks.project_create),
    app_link(vars.AppLinks.project_upload),
    app_link(vars.AppLinks.project_public_list),
    app_link(vars.AppLinks.project_public_anon_link),


    # Project URLs
    url_wrapper(vars.AppLinks.project_upload_progress),
    url_wrapper(vars.AppLinks.project_public_detail),
    url_wrapper(vars.AppLinks.project_detail),
    url_wrapper(vars.AppLinks.project_edit),
    url_wrapper(vars.AppLinks.project_mod_create),
    url_wrapper(vars.AppLinks.project_mod_edit),
    url_wrapper(vars.AppLinks.project_export_csv),
    url_wrapper(vars.AppLinks.project_public_request),
    url_wrapper(vars.AppLinks.project_public_widget),
    url_wrapper(vars.AppLinks.project_filter),

    # Locations Links and URLs
    # States, Parks, etc. in one model/object
    app_link(vars.AppLinks.locations),
    app_link(vars.AppLinks.location_create),
    url_wrapper(vars.AppLinks.location_detail),
    url_wrapper(vars.AppLinks.location_edit),
]
