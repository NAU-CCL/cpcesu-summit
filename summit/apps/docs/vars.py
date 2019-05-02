from config.links import DjangoLink, DjangoURL

from . import views

app_name = 'summit.apps.docs'
app_regex = r'^docs/'


class AppLinks:
    doc_detail = DjangoLink('doc_detail', app_name, app_regex,
                            r'^details/(?P<page_id>[-\w]+)/$', views.details,
                            'With This Page',
                            link_args={
                                'auth_required': True,
                                'side': 'right',
                                'dropdown_id': app_name,
                                'dropdown_name': 'Help'
                            })
    all_docs = DjangoLink('all_docs', app_name, app_regex, r'^$',
                          views.index, 'All Documents',
                          link_args={
                              'auth_required': True,
                              'side': 'right',
                              'dropdown_id': app_name
                          })
    doc_add_edit = DjangoLink('doc_add_edit', app_name, app_regex,
                              r'^form/(?P<page_id>[-\w]+)/$',
                              views.form,
                              'Add/Edit Document',
                              link_args={
                                  'auth_required': True,
                                  'side': 'right',
                                  'dropdown_id': app_name
                              })
