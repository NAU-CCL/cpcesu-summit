from django.conf.urls import url

from . import views

app_name = 'summit.apps.core'
urlpatterns = [
    url('', views.index),
    url(r'^index', views.index),
]
