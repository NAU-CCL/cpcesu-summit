from django.conf.urls import url

from . import views

# TODO: Create a redirect url for every organization

app_name = 'summit.apps.docs'
urlpatterns = [
    url(r'^public$', views.PublicView),
    url(r'^org$', views.OrgView),
    url(r'^cpcesu$', views.CPView),
    # url(r'^index', views.index),
]
