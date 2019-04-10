from django.conf.urls import url

from importlib import import_module
from django.utils import six


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

    add_link(regex, name, link_args)

    # Define URL
    vari = url(regex, view, kwargs, name)

    return vari


def add_link(regex, name, link_args=None):
    # Define Link
    new_link = dict()
    dropdown = None
    side = 'left'

    if link_args is None or not isinstance(link_args, dict):
        link_args = dict()

    # Find which div to add the link/dropdown to
    if 'side' in link_args and link_args['side'] == 'right':
        side = 'right'

    # If this link is a part of a dropdown
    if 'dropdown_id' in link_args and len(link_args['dropdown_id']) > 0:
        dropdown_id = link_args['dropdown_id']
        sel_links = links[0]
        # First, look for existing dropdown based on side
        if 'side' in link_args and link_args['side'] == 'right':
            sel_links = links[1]

        for index in range(len(sel_links)):
            if 'id' in sel_links[index] and sel_links[index]['id'] == dropdown_id:
                dropdown = index
                break
        # If it does not exist, make a new one
        if dropdown is None:
            dropdown = {'id': dropdown_id, 'links': [], 'name': link_args['dropdown_name'], 'type': 'dropdown'}

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

        if href[-1] != '/' and href[-1] != '$':
            href += '/'

        if href[0] == 'r':
            href = "/" + href[:1]
        if href[-1] == '$':
            href = href[:-1]
        href = href.strip('^$')

        if len(href) > 0 and href[0] != '/':
            href = '/' + href
        elif len(href) == 0:
            href = '/'

        new_link['link'] = href

    # If specified, add the app_regex so that it isn't root
    if 'app_regex' in link_args:
        href = str(link_args['app_regex'])
        href = href.strip('/').replace('^', '/')
        new_link['link'] = href + new_link['link']

    # Custom HTML classes
    if 'custom_classes' in link_args:
        new_link['custom_classes'] = link_args['custom_classes']

    # Description (title tag)
    if 'description' in link_args:
        new_link['description'] = link_args['description']

    # Auth options
    if 'auth_required' in link_args:
        new_link['auth_required'] = link_args['auth_required']

    if 'auth_perms' in link_args and 'auth_required' in new_link:
        new_link['auth_perms'] = link_args['auth_perms']

    # Is external link
    if 'target' in link_args:
        new_link['target'] = link_args['target']

    # Add link to left or right side of nav
    # If it doesn't belong to a dropdown
    if dropdown is None:
        if side == 'right':
            links[1].append(new_link)
        else:
            links[0].append(new_link)
    elif isinstance(dropdown, dict):
        dropdown['links'].append(new_link)
        if side == 'right':
            links[1].append(dropdown)
        else:
            links[0].append(dropdown)
    else:
        if side == 'right':
            links[1][dropdown]['links'].append(new_link)
        else:
            links[0][dropdown]['links'].append(new_link)


def get():
    return links
