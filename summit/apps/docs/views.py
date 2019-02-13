from django.shortcuts import render


def index(request, name):
    template_name = 'apps/docs/public_index.html'

    context = {
        'name': name,
        'pagetitle': 'Docs Index',
        'title': 'Docs Index',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
    }

    return render(request, template_name, context)

