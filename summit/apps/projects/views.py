from django.shortcuts import redirect, render
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Project


def index(request):

    template_name = 'apps/projects/project_index.html'



    return render(request, template_name, context)

# TODO: Refactor ProjectList() to display projects in order by title.


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'apps/projects/project_index.html'
    model = Project
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = {
            'pageId': 'apps.projects.index',
            'pagetitle': 'Projects',
            'title': 'Projects Overview',
            'bannerTemplate': 'none',
            'header': {
                'background': 'apps/core/imgs/default.jpg',
                'heading1': 'See how I got here and my future ambitions',
                'heading2': 'Looking towards the horizon',
                'buttons': [
                    # {
                    # 'name': 'My History',
                    # 'link': '/#button1'
                    # },
                    # {
                    # 'name': 'Download Resume',
                    # 'link': 'https://www.google.com/',
                    # 'target': '_blank'
                    # }
                ]
            },
            'cssFiles': [
            ]
        }
        ctx = super(ProjectListView, self).get_context_data(**kwargs)
        ctx = { **ctx, **context}
        return ctx

    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'pk':self})

class ProjectDetail(DeleteView):
    model = Project
    template_name = 'apps/projects/project_detail.html'

class ProjectCreate(CreateView):
    template_name = 'apps/projects/project_form.html'
    model = Project
    fields = ['project_title', 'short_summary', 'description', 'budget', 'student_support']