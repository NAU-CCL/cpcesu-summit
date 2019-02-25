from django.conf.urls import url

from . import views

app_name = 'summit.libs.auth'
urlpatterns = [
    url(r'^logged_out', views.logged_out),
    url(r'^profile', views.logged_out, name='profile')
]
