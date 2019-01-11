from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

def index(request):
    template_name = 'apps/docs/public_index.html'

    context = {
        'pageId': 'core.home',
        'pagetitle': 'Home',
        'title': 'Home page',
        # 'bannerTemplate': '',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
            # 'heading1': 'See how I got here and my future ambitions',
            # 'heading2': 'Looking towards the horizon',
            # 'buttons': [
            #     {
            #         'name': 'My History',
            #         'link': '/#button1'
            #     },
            #     {
            #         'name': 'Download Resume',
            #         'link': 'https://www.google.com/',
            #         'target': '_blank'
            #     }
            # ]
        },
        'cssFiles': [
        ]
    }

    if request.user.is_authenticated and request.user.is_staff:
        template_name = 'apps/docs/cp_index.html'

        context = {
            'pageId': 'core.home',
            'pagetitle': 'Home',
            'title': 'Home page',
            # 'bannerTemplate': 'fullscreen',
            'header': {
                'background': 'imgs/coverImages/default.jpg',
                # 'heading1': 'See how I got here and my future ambitions',
                # 'heading2': 'Looking towards the horizon',
                # 'buttons': [
                #     {
                #         'name': 'My History',
                #         'link': '/#button1'
                #     },
                #     {
                #         'name': 'Download Resume',
                #         'link': 'https://www.google.com/',
                #         'target': '_blank'
                #     }
                # ]
            },
            'cssFiles': [
            ]
        }

    elif request.user.is_authenticated:
        template_name = 'apps/docs/org_index.html'

        context = {
            'pageId': 'core.home',
            'pagetitle': 'Home',
            'title': 'Home page',
            # 'bannerTemplate': 'fullscreen',
            'header': {
                'background': 'imgs/coverImages/default-canyonlands.jpg',
                # 'heading1': 'See how I got here and my future ambitions',
                # 'heading2': 'Looking towards the horizon',
                # 'buttons': [
                #     {
                #         'name': 'My History',
                #         'link': '/#button1'
                #     },
                #     {
                #         'name': 'Download Resume',
                #         'link': 'https://www.google.com/',
                #         'target': '_blank'
                #     }
                # ]
            },
            'cssFiles': [
            ]
        }

    return render(request, template_name, context)

