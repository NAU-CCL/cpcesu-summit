from config.links import DjangoLink, DjangoURL

from . import views

app_name = 'summit.apps.core'
app_regex = ''


class AppLinks:
    index = DjangoLink('index', app_name, app_regex, r'^$', views.index,
                       'Home')
    about = DjangoLink('about', app_name, app_regex, r'^about/$', views.about,
                       'About')

    contact = DjangoLink('contact', app_name, app_regex, '', None, 'Contact',
                         link_args={
                             'link': 'https://in.nau.edu/cpesu/cpcesu-contact/',
                             'target': '_blank'
                         })
    admin_site = DjangoLink('admin_site', app_name, '', r'^/admin/$', None,
                            'Admin Site',
                            link_args={
                                'auth_required': True,
                                'side': 'right',
                                'staff_only': True
                            })