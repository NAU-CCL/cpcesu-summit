from config.links import DjangoLink, DjangoURL

from . import views

app_name = 'summit.apps.core'
app_regex = ''


class AppLinks:
    #index = DjangoURL('index', r'^$', views.index, app_name)
    about = DjangoLink('about', app_name, app_regex, r'^about/$', views.about,
                       'About')

    contact = DjangoLink('contact', app_name, app_regex, '', None, 'Contact',
                         link_args={
                             'link': 'https://in.nau.edu/cpesu/cpcesu-contact/',
                             'target': '_blank'
                         })
    tiles = DjangoLink('tiles', app_name, app_regex,
                                   r'^$', views.MainView.as_view(),
                                   'CESU Tiles'
                                   )