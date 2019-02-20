from config.links import link, get_name

from . import views

# TODO: Create a redirect url for every organization

app_name = 'summit.apps.docs'
app_regex = r'^docs/'
urlpatterns = [
    link(r'$', views.index, name=get_name(app_name, 'Documentation'), link_args={
        'side': 'right',
        'app_regex': app_regex,
    }),
]
