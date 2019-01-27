# TODO: Are we gonna use slugs? Yes. (Demo will just be inc.) Public facing.
# TODO: Set up urls to point to the projects views.py
from django.conf.urls import url

from . import views

app_name = 'summit.apps.projects'
urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(), name='project-list'),
    url(r'(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='project-detail'),
    url(r'add/$', views.ProjectCreate.as_view(), name='project-create'),
]
