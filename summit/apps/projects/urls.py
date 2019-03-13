# TODO: Circular import on reverse. Success of form should redirect to project_index
from django.conf import settings
from config.links import link, get_name
from django.conf.urls import url, include
from django.conf.urls.static import static

from . import views

app_name = 'summit.apps.projects'
app_regex = r'^projects/'
project_index = get_name(app_name, 'Projects')
urlpatterns = [
    link(r'^$', views.ProjectListView.as_view(), name=project_index, link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
        'dropdown_name': 'Projects'
    }),
    link(r'^redirect', views.project_form_redirect, name=get_name(app_name, 'Create Project'), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name
    }),
    url(r'^create', views.ProjectCreate.as_view(), name='project-create'),
    url(r'^detail/(?P<id>[-\w]+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^edit/(?P<id>[-\w]+)/$', views.ProjectEdit.as_view(), name='project-edit'),
    url(r'^autofill/', views.ProjectAutofill.as_view(), name='project-autofill'),
    url(r'^poll_state$', views.poll_state, name='poll_state'),
    url(r'^mods/(?P<id>[-\w]+)/$', views.ProjectModifications.as_view(), name='project-mods'),
    url(r'^detail/download_csv/(?P<id>[-\w]+)/$', views.export_to_csv, name='project-export-csv'),
]
