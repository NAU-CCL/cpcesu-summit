from config import links
from django import template

register = template.Library()


@register.inclusion_tag('partials/nav_links.html', takes_context=True)
def nav_links(context):
    try:
        name = context['name']
    except KeyError:
        name = "NONE"
        context['name'] = "NONE"
    nav_links_groups = links.get()

    nav_links_html = [
        [], []
    ]

    nav_links_html[0] = '<ul class="navbar-nav mr-auto">'
    nav_links_html[1] = '<ul class="navbar-nav ml-auto">'

    for index in range(len(nav_links_groups)):
        for link in nav_links_groups[index]:
            # Check auth
            if 'type' in link and link['type'] == 'dropdown':
                # Is dropdown
                nav_links_html[index] += create_link(link, context, True)
            else:
                # Is single link
                nav_links_html[index] += create_link(link, context, False)

    nav_links_html[0] += '</ul>'
    nav_links_html[1] += '</ul>'

    context['nav_links_left'] = nav_links_html[0]
    context['nav_links_right'] = nav_links_html[1]

    return context


def create_link(link_dict, context, is_dropdown_item):
    link_str = ''

    # if 'auth_required' in link_dict:
    #     print(link_dict)

    if 'auth_required' in link_dict and link_dict['auth_required'] and context['user'].is_authenticated() is False:
        return link_str

    if 'auth_perms' in link_dict and link_dict['auth_perms'] \
            and context['user'].has_perms(link_dict['auth_perms']) is False:
        return link_str

    link_str += '<li class="nav-item '

    # Is a dropdown dict
    if is_dropdown_item:
        link_str += ' dropdown">'

        link_str += '<a class="nav-link dropdown-toggle" id="' + link_dict['id'] + '" data-toggle="dropdown" '
        link_str += 'aria-haspopup="true" aria-expanded="false">' + link_dict['name'] + '</a>'

        link_str += '<div class="dropdown-menu dropdown-primary" aria-labelledby="' + link_dict['id'] + '">'

        # Used to track number of links in dropdown
        link_count = 0
        for link in link_dict['links']:
            link_str += '<a class="dropdown-item '

            if 'auth_required' in link and link['auth_required'] and context[
                'user'].is_authenticated() is False:
                continue

            if 'auth_perms' in link and link['auth_perms'] \
                    and context['user'].has_perms(link['auth_perms']) is False:
                continue

            if link['name'] == context['name']:
                link_str += 'active '
            if 'custom_classes' in link and link['custom_classes']:
                link_str += link['custom_classes'] + ' '

            link_str += '" title="' + link['description'] if 'description' in link_dict else link['label']

            # Making actual nav link
            link_str += '" href="' + link['link'] + '" target="'

            if 'target' in link and link['target']:
                link_str += link['target'] + '">'
            else:
                link_str += '">'

            link_str += link['label'] + '</a>'
            link_count += 1

        link_str += '</div>'

        if link_count == 0:
            return ''
    # Single item
    else:
        if link_dict['name'] == context['name']:
            link_str += 'active '
        if 'custom_classes' in link_dict and link_dict['custom_classes']:
            link_str += link_dict['custom_classes'] + ' '

        link_str += '" title="' + link_dict['description'] if 'description' in link_dict else link_dict['label'] + '">'

        # Making actual nav link
        link_str += '<a class="nav-link" href="' + link_dict['link'] + '" target="'

        if 'target' in link_dict and link_dict['target']:
            link_str += link_dict['target'] + '">'
        else:
            link_str += '">'

        link_str += link_dict['label'] + '</a>'

    link_str += '</li>'

    return link_str
