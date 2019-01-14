from django.conf.urls import url

from django.urls import reverse


# Nav links
links = [
    [],
    []
]


def get_name(app_name, name):
    return app_name + "_" + name


def link(regex, view, name, kwargs=None, link_args=None):
    if kwargs is None or kwargs == {}:
        kwargs = dict()

    if not hasattr(kwargs, 'name'):
        kwargs['name'] = name

    # Define URL
    vari = url(regex, view, kwargs, name)

    add_link(regex, name, link_args)

    return vari


def add_link(regex, name, link_args=None):
    # Define Link
    new_link = dict()

    if link_args is None or not isinstance(link_args, dict):
        link_args = dict()

    # Get Link Name (app_name + view name) and Label (shown to user
    new_link['name'] = link_args['name'] if 'name' in link_args else name
    new_link['label'] = link_args['label']\
        if 'label' in link_args\
        else str.split(name, '_')[-1]

    # Get Link/href
    if 'link' in link_args:
        new_link['link'] = link_args['link']
    else:
        href = str(regex)
        href += '/' if href[0] != '/' else ''
        href = href.replace('r', '/').strip('$^')
        new_link['link'] = href

    # Custom HTML classes
    if 'custom_classes' in link_args:
        new_link['custom_classes'] = link_args['custom_classes']

    # Description (title tag)
    if 'description' in link_args:
        new_link['description'] = link_args['description']

    # Auth options
    if 'auth_required' in link_args:
        new_link['auth_required'] = link_args['auth_required']

    if 'staff_only' in link_args and 'auth_required' in new_link:
        new_link['staff_only'] = link_args['staff_only']

    # Add link to left or right side of nav
    if 'side' in link_args and link_args['side'] == 'right':
        links[1].append(new_link)
    else:
        links[0].append(new_link)


def get():
    return links
