# TODO: Are we gonna use slugs? Yes. (Demo will just be inc.) Public facing.
from django.conf.urls import url

from . import views

app_name = 'summit.apps.core'
urlpatterns = [
    url(r'^$', views.index),
    # url(r'^index', views.index),
]
