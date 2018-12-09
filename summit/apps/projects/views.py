from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
from django.views.generic import ListView

from .models import Project


def index(request):
    template_name = 'apps/projects/project_index.html'

    context = {
        'pageId': 'core.home',
        'pagetitle': 'Projects',
        'title': 'Project page',
        'bannerTemplate': 'fullscreen',
        # 'header': {
        #     'background': 'apps/core/imgs/default.jpg',
        #     'heading1': 'See how I got here and my future ambitions',
        #     'heading2': 'Looking towards the horizon',
        #     'buttons':[
        #         # {
        #         # 'name': 'My History',
        #         # 'link': '/#button1'
        #         # },
        #         # {
        #         # 'name': 'Download Resume',
        #         # 'link': 'https://www.google.com/',
        #         # 'target': '_blank'
        #         # }
        #     ]
        # },
        'cssFiles': [
            'css/apps/core/testing.css'
        ]
    }

    return render(request, template_name, context)

# TODO: Refactor ProjectList() to display projects in order by title.


class ProjectList(ListView):
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.order_by('project_title')

