from config.links import link, get_name

from . import views

# TODO: Create a redirect url for every organization

app_name = 'summit.apps.docs'
urlpatterns = [
    link(r'$', views.index, get_name(app_name, 'Documentation'), link_args={
        'custom_classes': 'btn btn-primary btn-sm',
        'side': 'right'
    }),
]
