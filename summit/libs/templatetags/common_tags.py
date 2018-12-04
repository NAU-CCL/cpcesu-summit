from summit.libs import links
from django import template

register = template.Library()

@register.inclusion_tag('partials/navLinks.html', takes_context=True)
def navLinks(context):
    try:
        pageId = context['pageId']
    except KeyError:
        pageId = "NONE"
    navLinks = links.get()
    return {'navLinks': navLinks, 'pageId': pageId}
