from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Project, Notification
from .forms import ProjectForm

def index_view(request):
    notifications = Notification.objects.all()
    return render(request, 'apps/projects/project_index.html', {'notifications': notifications})
# class IndexView(ListView):
#     model = Notification
#     template_name = 'apps/projects/project_index.html'
#     context_object_name = 'notifications'
#
#     def get_context_data(self, **kwargs):
#         context = {'type': self.kwargs['type']}
#         ctx = super(IndexView, self).get_context_data(**kwargs)
#         ctx = {**ctx, **context}
#         return ctx


    #def get_context_data(self, **kwargs):
        #return Project.objects.all()

# TODO: Refactor ProjectList() to display projects in order by title.


class ProjectListView(LoginRequiredMixin, ListView):
    template_name = 'apps/projects/project_index.html'
    model = Project
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = {
            'name': self.kwargs['name'],
            'notifications': Notification.objects.all(),
            'pagetitle': 'Home',
            'title': 'Home page',
            # 'bannerTemplate': 'fullscreen',
            'header': {
                # 'background': 'apps/core/imgs/default.jpg',
                # 'heading1': 'Heading 1',
                # 'heading2': 'Heading 2',
                # 'buttons': [
                #     {
                #         'name': 'Button 1',
                #         'link': '/#button1'
                #     },
                #     {
                #         'name': 'External Button',
                #         'link': 'https://www.google.com/',
                #         'target': '_blank'
                #     }
                # ]
            },
            'cssFiles': [
                # 'css/apps/core/testing.css'
            ]
        }
        ctx = super(ProjectListView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'pk':self})


# class ProjectDetail(DetailView):
#     model = Project
#     template_name = 'apps/projects/project_detail.html'
#
#     def get_object(self, **kwargs):
#         pk_ = self.kwargs.get("pk")
#         return get_object_or_404(Project, pk=pk_)


class ProjectCreate(CreateView):
    template_name = 'apps/projects/project_form.html'
    model = Project
    form_class = ProjectForm
