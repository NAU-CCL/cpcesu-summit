from django.conf.urls import url, include

from . import views

app_name = 'summit.apps.core'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^docs/', include('summit.apps.docs.urls')),
    # url(r'^index', views.index),
]
