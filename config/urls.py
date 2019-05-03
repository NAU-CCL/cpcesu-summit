"""summit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from summit.libs.auth.vars import app_regex as auth_regex, app_name as auth_name


from summit.apps.docs.vars import app_regex as docs_regex, app_name as docs_name
from summit.apps.projects.vars import app_regex as project_regex, app_name as project_name

from rest_framework import routers
from summit.apps.projects import views
# REST Endpoints
router = routers.DefaultRouter()
router.register(r'federal_agencies', views.FederalAgencyViewSet)
router.register(r'partners', views.PartnerViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(auth_regex, include('django.contrib.auth.urls')),
    url(auth_regex, include(auth_name + '.urls')),
    url('', include('summit.apps.core.urls')),
    url(docs_regex, include(docs_name + '.urls')),
    url(project_regex, include(project_name + '.urls')),
    url(auth_regex, include(auth_name + '.urls2')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
              + static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = 'summit.libs.views.error400'
handler403 = 'summit.libs.views.error403'
handler404 = 'summit.libs.views.error404'
handler500 = 'summit.libs.views.error500'

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
