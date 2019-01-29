from django.shortcuts import get_object_or_404, render


def index(request, name):
    template_name = 'apps/core/index.html'

    context = {
        'name': name,
        'pagetitle': 'Home',
        'title': 'Home page',
        'bannerTemplate': 'fullscreen',
        'header': {
            # 'background': 'apps/core/imgs/default.jpg',
            'heading1': 'Heading 1',
            'heading2': 'Heading 2',
            'buttons': [
                {
                    'name': 'Button 1',
                    'link': '/#button1'
                },
                {
                    'name': 'External Button',
                    'link': 'https://www.google.com/',
                    'target': '_blank'
                }
            ]
        },
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ]
    }

    return render(request, template_name, context)


def about(request, name):
    template_name = 'apps/core/about.html'

    context = {
        'name': name,
        'pagetitle': 'About',
        'title': 'About the CPCESU',
        'header': {
            'background': 'imgs/coverImgs//canyon-country-2400x600.jpg',
        },
    }

    return render(request, template_name, context)

