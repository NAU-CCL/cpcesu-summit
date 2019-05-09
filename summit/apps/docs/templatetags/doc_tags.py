from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from summit.apps.docs.models import Document
from summit.apps.docs.vars import AppLinks, app_name

register = template.Library()


@register.simple_tag(takes_context=True)
def help_docs(context):
    user = context.request.user
    link_template = '<a class="dropdown-item waves-effect waves-light" href="#" onClick="MyWindow=window.open(\' %s \',\'MyWindow\',width=300,height=300); return false;"> %s </a>'

    # Get document ID
    url_path = context.request.path
    url_path = url_path.split("/")[1:]

    doc_id = []
    for url in url_path:
        if not any(char.isdigit() for char in url):
            doc_id.append(url)
    doc_id = '/'.join(doc_id)

    # Defaults to home page documentation
    if doc_id is not None and len(doc_id) == 0:
        doc_id = '/'

    if doc_id is not None:
        # Now, check database for doc id
        try:
            doc = Document.objects.get(page_id=doc_id)
        except ObjectDoesNotExist:
            doc = None

    else:
        doc = None

    doc_href = ""
    # If doc exists and published
    if doc and doc.is_published:
        print("exists and published")
        # If doc is public
        if doc.is_public or (doc.is_public is False and user.is_authenticated):
            print("has perm!")
            doc_url = reverse(app_name + ':' + AppLinks.doc_detail.ident) + "?page_id=" + doc_id
            doc_href = link_template % (doc_url, 'With This Page')

    editor_href = ""
    if user.is_authenticated and user.is_superuser:
        editor_url = reverse(app_name + ':' + AppLinks.doc_add_edit.ident) + "?page_id=" + doc_id
        editor_href = link_template % (editor_url, 'Add/Edit Doc')

    all_docs_url = reverse(app_name + ':' + AppLinks.all_docs.ident)
    all_docs_href = link_template % (all_docs_url, 'All Docs')

    if context.request.user.is_authenticated:
        link = '<li class="nav-item dropdown"> \
                  <a class="nav-link dropdown-toggle waves-effect waves-light" id="summit.apps.docs" data-toggle="dropdown" aria-haspopup="true">Help</a>\
                  <div class="dropdown-menu dropdown-primary" aria-labelledby="summit.apps.docs"> \
                     ' + doc_href + '\
                     ' + all_docs_href + '\
                     ' + editor_href + '\
                  </div>\
                </li>'
    elif len(doc_href) > 0:
        link = '<li class="nav-item">\
            <a class="nav-link waves-effect waves-light" href="#" onClick="MyWindow=window.open(\'' + doc_url + '\',\'MyWindow\',width=300,height=300); return false;" target="_blank">\
            Help</a></li>'
    else:
        link = '';
    return link