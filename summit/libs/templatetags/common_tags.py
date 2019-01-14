from config import links
from django import template

register = template.Library()


@register.inclusion_tag('partials/navLinks.html', takes_context=True)
def navLinks(context):
    try:
        name = context['name']
    except KeyError:
        context['name'] = "NONE"
    navLinks = links.get()

    context['navLinksLeft'] = navLinks[0]
    context['navLinksRight'] = navLinks[1]

    return context
