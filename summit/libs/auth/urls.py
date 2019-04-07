from config.links import link, get_name
from django.conf.urls import url

from . import views

app_name = 'summit.libs.auth'
app_regex = r'^projects/'
urlpatterns = [
    url(r'^logged_out', views.logged_out),
    url(r'^edit_profile', views.edit_profile, name='edit_profile'),
    url(r'^profile', views.view_profile, name='view_profile'),
]
