from config.links import DjangoLink, DjangoURL

from . import views

app_name = "summit.libs.auth"
app_regex = r'^accounts/'


class AppLinks:
    #
    #
    # Primary links in the nav menu (load in first/separate)
    #
    #
    logged_out = DjangoURL('logged_out', r'^logged_out/$', views.logged_out, app_name)
    edit_contact = DjangoURL('edit_contact', r'^edit_contact/(?P<profile_id>[-\w]+)/$', views.edit_contact, app_name)
    edit_my_contact = DjangoURL('edit_my_contact', r'^edit_contact/$', views.edit_contact, app_name)
    view_my_contact = DjangoURL('view_my_contact', r'^view_contact/$', views.view_contact, app_name)
    view_contact = DjangoURL('view_contact', r'^view_contact/(?P<profile_id>[-\w]+)/$', views.view_contact, app_name)

    #
    #
    # Secondary Links in nav menu (load in second/separate)
    #
    #
    cesu_selector = DjangoLink('cesu_selector', app_name, app_regex,
                                r'^cesu_selector/$', views.CESUSwitcherView.as_view(),
                                'CESU Selector',
                                link_args={
                                    'auth_required': True
                                })

    all_contacts = DjangoLink('all_contacts', app_name, app_regex,
                              r'^all_contacts/$', views.all_contacts, 'All Contacts',
                              link_args={
                                  'auth_required': True,
                                  'dropdown_id': app_name,
                                  'dropdown_name': 'Personnel'
                              })
    all_organizations = DjangoLink('all_organizations', app_name, app_regex, r'^all_groups/$',
                                   views.all_organizations, 'All Organizations',
                                   link_args={
                                       'auth_required': True,
                                       'dropdown_id': app_name,
                                   })

    create_organization = DjangoLink('create_organization', app_name, app_regex, r'^create_organization/$',
                                     views.create_organization, 'Create Organization',
                                     link_args={
                                         'auth_required': True,
                                         'dropdown_id': app_name,
                                     })

    create_contact = DjangoLink('create_contact', app_name, app_regex, r'^create_contact/$', views.create_contact,
                                'Create Contact',
                                link_args={
                                    'auth_required': True,
                                    'dropdown_id': app_name
                                })

    manage_my_organization = DjangoLink('manage_my_organization', app_name, app_regex, r'^manage_organization/$',
                                        views.manage_organization, 'Manage My Organization',
                                        link_args={
                                            'auth_required': True,
                                            'dropdown_id': app_name
                                        })

    # URLs
    manage_organization = DjangoURL('manage_organization', r'^manage_organization/(?P<group_id>[-\w]+)/$',
                                    views.manage_organization, app_name)

    edit_organization = DjangoURL('edit_organization', r'^edit_organization/(?P<group_id>[-\w]+)/$',
                                  views.edit_organization, app_name)

    create_contact_in_group = DjangoURL('create_contact_in_group', r'^create_contact/(?P<group_id>[-\w]+)/$',
                                        views.create_contact, app_name)
    info_display = DjangoURL('info_display', r'^info_display/$', views.info_display, app_name)
    org_info = DjangoURL('org_info', r'^org_info/$', views.org_info, app_name)


