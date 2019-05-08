from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def help_docs(context):

    # Get document ID
    doc_id = context.request.path
    doc_id = doc_id.split("/")[1:3]
    doc_id = '/'.join(doc_id)
    print(doc_id)

    # Now, check database for doc id

    if context.request.user.is_authenticated:
        link = '<li class="nav-item dropdown"> \
                  <a class="nav-link dropdown-toggle waves-effect waves-light" id="summit.apps.docs" data-toggle="dropdown" aria-haspopup="true">Help</a>\
                  <div class="dropdown-menu dropdown-primary" aria-labelledby="summit.apps.docs"> \
                     <a class="dropdown-item waves-effect waves-light" href="#test1">With This Page</a>\
                     <a class="dropdown-item waves-effect waves-light" href="#test2">All Docs</a>\
                     <a class="dropdown-item waves-effect waves-light" href="#test3">Add/Edit Doc</a>\
                  </div>\
                </li>'
    else:
        # link = '<li class="nav-item"> \
        #   <a class="nav-link waves-effect waves-light" href="#test" target="_blank">Help</a>\
        # </li>'
        link = ''
    return link