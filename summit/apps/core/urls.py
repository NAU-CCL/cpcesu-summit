from config.links import get_name, link, add_link

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'summit.apps.core'
urlpatterns = [
    link(r'^$', views.index, get_name(app_name, 'Home')),
    link(r'^about/$', views.about, get_name(app_name, 'About'))
]

add_link('', get_name(app_name, 'Contact'), {
    'link': 'https://in.nau.edu/cpesu/cpcesu-contact/',
    'target': '_blank'
})

# Static links
add_link('/admin/$', get_name(app_name, 'Admin Site'), {
    'auth_required': True,
    'side': 'right',
    'staff_only': True
})
# TODO: Only should we serve files in this way when we're developing - Colton
urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# add_link('/', get_name(app_name, 'Send Feedback'), {
#     'custom_classes': 'btn btn-primary btn-sm',
#     'side': 'right'
# })



