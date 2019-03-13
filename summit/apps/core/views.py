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
            'heading1': 'Welcome to Summit',
            'heading2': 'Your New Cooperative Ecosystem Studies Unit Project Management System',
            'buttons': [
                {
                    'name': 'About Summit',
                    'link': "summit.apps.core:summit.apps.core_About",
                    'uses_reverse': True
                },
                {
                    'name': 'Current Projects',
                    'link': "summit.apps.projects:summit.apps.projects_Projects",
                    'uses_reverse': True
                    # 'target': '_blank'
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
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
    }

    return render(request, template_name, context)
