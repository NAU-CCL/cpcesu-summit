# TODO: Are we gonna use slugs? Yes. (Demo will just be inc.) Public facing.
# TODO: Set up urls to point to the projects views.py
from django.conf.urls import url

from .views import ProjectListView

app_name = 'summit.apps.projects'
urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='project-list'),
]
