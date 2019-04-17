from django.shortcuts import render


def index(request, name):
    template_name = 'apps/docs/doc_index.html'

    context = {
        'name': name,
        'pagetitle': 'Docs Index',
        'title': 'Docs Index',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
    }

    return render(request, template_name, context)


def details(request, name):
    template_name = 'apps/docs/doc_details.html'

    context = {
        'name': name,
        'pagetitle': 'Docs Details',
        'title': 'Docs Details',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
    }

    return render(request, template_name, context)


def form(request, name):
    template_name = 'apps/docs/doc_form.html'

    context = {
        'name': name,
        'pagetitle': 'Docs Form',
        'title': 'Docs Form',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
    }

    return render(request, template_name, context)
