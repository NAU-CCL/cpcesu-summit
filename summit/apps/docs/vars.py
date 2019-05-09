from config.links import DjangoURL

from . import views

app_name = 'summit.apps.docs'
app_regex = r'^docs/'


class AppLinks:
    doc_detail = DjangoURL('doc_detail', r'^details/$', views.details, app_name)
    all_docs = DjangoURL('all_docs', r'^$', views.index, app_name)
    doc_add_edit = DjangoURL('doc_add_edit', r'^form/$', views.form, app_name)
