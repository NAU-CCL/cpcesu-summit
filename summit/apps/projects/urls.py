# TODO: Circular import on reverse. Success of form should redirect to project_index
from django.conf import settings
from config.links import link, get_name
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

app_name = 'summit.apps.projects'
app_regex = r'^projects/'
urlpatterns = [
    # Projects and Modifications

    link(r'^dashboard/$', views.ProjectDashboardView.as_view(), name=get_name(app_name, "Your Dashboard"), link_args={
        'auth_required': True,
        'app_regex': app_regex
    }),
    link(r'^$', views.ProjectListView.as_view(), name=get_name(app_name, "All Projects"), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
        'dropdown_name': 'Projects'
    }),
    link(r'^autofill/$', views.project_autofill, name=get_name(app_name, 'Autofill Project'), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name
    }),
    link(r'^create/$', views.ProjectCreate.as_view(), name=get_name(app_name, 'Create Project'), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name
    }),
    link(r'^public_projects/$', views.ProjectPublicListView.as_view(), name=get_name(app_name, 'Public Projects'), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name,
    }),
    link(r'^public_projects/$', views.ProjectPublicListView.as_view(), name=get_name(app_name, 'Public Projects'), link_args={
        'auth_required': False,
        'app_regex': app_regex,
    }),
    url(r'^public-detail/(?P<id>[-\w]+)/$', views.ProjectPublicDetail.as_view(), name='project-detail-public'),
    url(r'^detail/(?P<id>[-\w]+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^edit/(?P<id>[-\w]+)/$', views.ProjectEdit.as_view(), name='project-edit'),
    url(r'^mods/(?P<id>[-\w]+)/create/$', views.ProjectModifications.as_view(), name='project-mods'),
    url(r'^mods/(?P<id>[-\w]+)/edit/(?P<mod_id>[-\w]+)$', views.ProjectModEdit.as_view(), name='project-mods-edit'),
    url(r'^export_csv/$', views.export_to_csv, name='project-export-csv'),
    url(r'^detail/change_history/(?P<id>[-\w]+)/$', views.change_history, name='project-change-history'),

    # Locations - States, Parks, etc. in one model/object
    link(r'^locations/$', views.LocationListView.as_view(), name=get_name(app_name, "Manage Locations"), link_args={
        'auth_required': True,
        'app_regex': app_regex,
        'dropdown_id': app_name
    }),
    url(r'^locations/create/$', views.LocationCreate.as_view(), name="location-create", kwargs={
        "name": get_name(app_name, "Create Location")
    }),
    url(r'^locations/detail/(?P<id>[-\w]+)/$', views.LocationDetail.as_view(), name='location-detail'),
    url(r'^locations/edit/(?P<id>[-\w]+)/$', views.LocationEdit.as_view(), name='location-edit'),
]
