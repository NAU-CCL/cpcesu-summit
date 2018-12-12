from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

def index(request):
    template_name = 'apps/docs/index.html'

    context = {
        'pageId': 'core.home',
        'pagetitle': 'Home',
        'title': 'Home page',
        'bannerTemplate': 'fullscreen',
        'header': {
            'background': 'apps/core/imgs/default.jpg',
            'heading1': 'See how I got here and my future ambitions',
            'heading2': 'Looking towards the horizon',
            'buttons':[
                {
                'name': 'My History',
                'link': '/#button1'
                },
                {
                'name': 'Download Resume',
                'link': 'https://www.google.com/',
                'target': '_blank'
                }
            ]
        },
        'cssFiles': [
            'css/apps/core/testing.css'
        ]
    }

    return render(request, template_name, context)

def PublicView(request):
    template_name = 'apps/docs/public_index.html'

    context = {
        'pageId': 'core.home',
        'pagetitle': 'Home',
        'title': 'Home page',
        'bannerTemplate': 'fullscreen',
        'header': {
            'background': 'apps/core/imgs/default.jpg',
            'heading1': 'See how I got here and my future ambitions',
            'heading2': 'Looking towards the horizon',
            'buttons':[
                {
                'name': 'My History',
                'link': '/#button1'
                },
                {
                'name': 'Download Resume',
                'link': 'https://www.google.com/',
                'target': '_blank'
                }
            ]
        },
        'cssFiles': [
            'css/apps/core/testing.css'
        ]
    }

    return render(request, template_name, context)


def OrgView(request):
    template_name = 'apps/docs/org_index.html'

    context = {
        'pageId': 'core.home',
        'pagetitle': 'Home',
        'title': 'Home page',
        'bannerTemplate': 'fullscreen',
        'header': {
            'background': 'apps/core/imgs/default.jpg',
            'heading1': 'See how I got here and my future ambitions',
            'heading2': 'Looking towards the horizon',
            'buttons':[
                {
                'name': 'My History',
                'link': '/#button1'
                },
                {
                'name': 'Download Resume',
                'link': 'https://www.google.com/',
                'target': '_blank'
                }
            ]
        },
        'cssFiles': [
            'css/apps/core/testing.css'
        ]
    }

    return render(request, template_name, context)


# CPCESU View
def CPView(request):
    template_name = 'apps/docs/cp_index.html'

    context = {
        'pageId': 'core.home',
        'pagetitle': 'Home',
        'title': 'Home page',
        'bannerTemplate': 'fullscreen',
        'header': {
            'background': 'apps/core/imgs/default.jpg',
            'heading1': 'See how I got here and my future ambitions',
            'heading2': 'Looking towards the horizon',
            'buttons':[
                {
                'name': 'My History',
                'link': '/#button1'
                },
                {
                'name': 'Download Resume',
                'link': 'https://www.google.com/',
                'target': '_blank'
                }
            ]
        },
        'cssFiles': [
            'css/apps/core/testing.css'
        ]
    }

    return render(request, template_name, context)

