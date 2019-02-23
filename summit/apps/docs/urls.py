from django.conf.urls import url

from config.links import link, get_name

from . import views

# TODO: Create a redirect url for every organization

app_name = 'summit.apps.docs'
app_regex = r'^docs/'
urlpatterns = [
    url(r'^$', views.index, kwargs={"name": get_name(app_name, 'doc-index')})
    # url(r'^$', views.index, get_name(app_name, 'Docs Index')),
    # link(r'$', views.index, name=get_name(app_name, 'Read Docs'), link_args={
    #     'side': 'right',
    #     'app_regex': app_regex,
    #     'dropdown_id': app_name,
    #     'dropdown_name': 'Documentation'
    # }),
    # link(r'$', views.index, name=get_name(app_name, 'Add/Edit Doc'), link_args={
    #     'side': 'right',
    #     'auth_required': True,
    #     'app_regex': app_regex,
    #     'dropdown_id': app_name,
    # }),
    # link(r'$', views.index, name=get_name(app_name, 'All Docs'), link_args={
    #     'side': 'right',
    #     'app_regex': app_regex,
    #     'dropdown_id': app_name,
    # }),
]
