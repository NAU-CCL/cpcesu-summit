from config.links import DjangoLink, DjangoURL

from . import views

app_name = 'summit.apps.projects'
app_regex = r'^projects/'


class AppLinks:
    # All Links - ORDER MATTERS
    # Single Link

    project_dashboard = DjangoLink('project_dashboard', app_name, app_regex,
                                   r'^dashboard/$', views.ProjectDashboardView.as_view(),
                                   'Your Dashboard',
                                   link_args={
                                       'auth_required': True
                                   })

    project_upload_dashboard = DjangoLink('project_upload_dashboard', app_name, app_regex,
                                   r'^upload_dashboard/$', views.ProjectUploadView.as_view(),
                                   'Your Uploading Dashboard',
                                   link_args={
                                       'auth_required': True
                                   })

    # Dropdown Menu/Links
    all_projects = DjangoLink('all_projects', app_name, app_regex, r'^$',
                              views.ProjectListView.as_view(), 'All Projects',
                              link_args={
                                  'auth_required': True,
                                  'dropdown_id': app_name,
                                  'dropdown_name': 'Projects'
                              })
    project_create = DjangoLink('project_create', app_name, app_regex,
                                r'^create/', views.ProjectCreate.as_view(),
                                'Create Project',
                                link_args={
                                    'auth_required': True,
                                    'dropdown_id': app_name
                                })

    project_upload = DjangoLink('project_upload', app_name, app_regex,
                                r'^autofill/$', views.ProjectAutofill.as_view(),
                                'Upload Project',
                                link_args={
                                    'auth_required': True,
                                    'dropdown_id': app_name
                                })

    project_public_list = DjangoLink('project_public_list', app_name, app_regex,
                                     r'^public_projects/$',
                                     views.ProjectPublicListView.as_view(),
                                     'Public Projects',
                                     link_args={
                                         'auth_required': True,
                                         'dropdown_id': app_name
                                     })

    project_public_anon_link = DjangoLink('project_public_anon_link', app_name, app_regex,
                                          r'^public_projects/$',
                                          views.ProjectPublicListView.as_view(),
                                          'Public Projects',
                                          link_args={'auth_required': False})

    # All URLs
    project_upload_progress = DjangoURL('project_upload_progress',
                                        r'^progress/$',
                                        views.ProjectProgress.as_view(),
                                        app_name)

    project_public_detail = DjangoURL('project_public_detail',
                                      r'^public-detail/(?P<id>[-\w]+)/$',
                                      views.ProjectPublicDetail.as_view(),
                                      app_name)

    project_detail = DjangoURL('project_detail', r'^detail/(?P<id>[-\w]+)/$',
                               views.ProjectDetail.as_view(), app_name)
    project_edit = DjangoURL('project_edit', r'^edit/(?P<id>[-\w]+)/$',
                             views.ProjectEdit.as_view(), app_name)
    project_mod_create = DjangoURL('project_mod_create',
                                   r'^mods/(?P<id>[-\w]+)/create/$',
                                   views.ProjectModifications.as_view(),
                                   app_name)
    project_mod_edit = DjangoURL('project_mod_edit',
                                 r'^mods/(?P<id>[-\w]+)/edit/(?P<mod_id>[-\w]+)$',
                                 views.ProjectModEdit.as_view(), app_name)
    project_export_csv = DjangoURL('project_export_csv', r'^export_csv/$',
                                   views.export_to_csv, app_name)
    project_public_request = DjangoURL('project_public_request', r'^public-request/(?P<project_id>[-\w]+)/$',
                                       views.request_project_info, app_name)
    project_public_widget = DjangoURL('project_public_widget', r'^public-widget/',
                                      views.ProjectPublicListView.as_view(), app_name, kwargs={"is_widget": True})
    project_filter = DjangoURL('project_filter', r'^filter/', views.project_filter, app_name)
    project_search = DjangoURL('project_search', r'^search/', views.project_search, app_name)
    change_cesu = DjangoURL('change_cesu', r'^change_cesu/', views.change_cesu, app_name)

    file_upload = DjangoURL('file_upload', r'^upload/', views.file_upload, app_name)
    delete_file = DjangoURL('delete_file', r'^delete_file/', views.delete_file, app_name)
    unarchive_project = DjangoURL('unarchive_project', r'^unarchive_project/', views.unarchive_project, app_name)
    archive_project = DjangoURL('archive_project', r'^archive_project/', views.archive_project, app_name)

    # Location Related Links/URLs
    # States, Parks, etc. in one model/object
    locations = DjangoLink('locations', app_name, app_regex, r'^locations/$',
                           views.LocationListView.as_view(), 'Manage Locations',
                           link_args={
                               'auth_required': True,
                               'dropdown_id': app_name
                           })
    location_create = DjangoLink('location_create', app_name, app_regex,
                                 r'^locations/create/$',
                                 views.LocationCreate.as_view(),
                                 'Create Location',
                                 link_args={
                                     'auth_required': True,
                                     'dropdown_id': app_name
                                 })
    location_detail = DjangoURL('location_detail',
                                r'^locations/detail/(?P<id>[-\w]+)/$',
                                views.LocationDetail.as_view(), app_name)

    location_edit = DjangoURL('location_edit',
                              r'^locations/edit/(?P<id>[-\w]+)/$',
                              views.LocationEdit.as_view(), app_name)
