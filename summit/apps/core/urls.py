from django.conf.urls import url, include

from . import views

app_name = 'summit.apps.core'
urlpatterns = [
    url(r'^$', views.index),
    # url(r'^index', views.index),
]
