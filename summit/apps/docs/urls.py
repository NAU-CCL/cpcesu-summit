from django.conf.urls import url

from . import views

# TODO: Create a redirect url for every organization

app_name = 'summit.apps.docs'
urlpatterns = [
    url(r'$', views.index),
]
