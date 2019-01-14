from config.links import get_name, link, add_link

from . import views


app_name = 'summit.apps.core'
urlpatterns = [
    link(r'^$', views.index, get_name(app_name, 'Home')),
    link(r'^about/', views.about, get_name(app_name, 'About')),
    link(r'^$', views.index, get_name(app_name, 'Contact')),
]

# Static links
add_link('/admin', get_name(app_name, 'Admin Site'), {
    'auth_required': True,
    'side': 'right',
    'staff_only': True
})

add_link('/', get_name(app_name, 'Send Feedback'), {
    'custom_classes': 'btn btn-primary btn-sm',
    'side': 'right'
})