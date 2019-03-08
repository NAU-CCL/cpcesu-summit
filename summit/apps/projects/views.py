from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from .models import Project, Notification
from .forms import ProjectForm
from .tasks import add


def mark_seen(request):
    notification = Notification.objects.get(pk=pk)
    notification.seen = True
    notification.save()


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'apps/projects/project_index.html'
    model = Project
    context_object_name = 'projects'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    raise_exception = True

    def get_context_data(self, **kwargs):
        add_result1 = add.apply_async((2, 2))
        add_result2 = add.delay(2, 2)
        print("add_result-status: " + str(add_result1.status))
        print("Backend: " + str(add_result1.backend))
        print("Backend: " + str(add_result2.backend))
        print("add_result: " + str(add_result1.get()))
        print("add_result: " + str(add_result2.get()))
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Projects List',
            'title': 'Projects List',
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
                'libs/mdb/css/addons/datatables.min.css',
                'css/apps/projects/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/apps/projects/dashboard.js'
            ]
        }
        ctx = super(ProjectListView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    # TODO: integrate this get_obkect into context
    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


# TODO: Change context object name
class ProjectDetail(DetailView):
    model = Project
    template_name = 'apps/projects/project_detail.html'

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectCreate(CreateView):
    template_name = 'apps/projects/project_form.html'
    model = Project
    form_class = ProjectForm


class ProjectEdit(UpdateView):
    template_name = 'apps/projects/project_form.html'
    model = Project
    form_class = ProjectForm

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)

