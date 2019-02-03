# TODO: Circular import on reverse. Success of form should redirect to project_index
from config.links import link, get_name

from . import views

app_name = 'summit.apps.projects'
app_regex = r'^projects/'
project_index = get_name(app_name, 'Projects')
urlpatterns = [
    link('^$', views.ProjectListView.as_view(), name=project_index, link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
        'dropdown_name': 'Projects'
    }),
    link(r'^create', views.ProjectCreate.as_view(), name=get_name(app_name, 'Create Project'), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name
    }),
]
