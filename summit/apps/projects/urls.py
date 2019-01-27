# TODO: Are we gonna use slugs? Yes. (Demo will just be inc.) Public facing.
# TODO: Set up urls to point to the projects views.py
from config.links import link, get_name

from . import views

app_name = 'summit.apps.projects'
urlpatterns = [
    link(r'^$', views.ProjectListView.as_view(), name=get_name(app_name, 'Projects'), link_args={
        'auth_required': True
    }),
]
