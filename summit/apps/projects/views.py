import csv
from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from .models import Project, File
from .forms import ProjectForm, ProjectFileForm


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'apps/projects/project_index.html'
    model = Project
    context_object_name = 'projects'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    raise_exception = False

    def get_context_data(self, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = {
            # 'name': self.kwargs['name'],
            'pagetitle': 'Projects Details',
            'title': 'Projects Details',
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
        ctx = super(ProjectDetail, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        ctx['files'] = File.objects.filter(project=self.object)
        # ctx['history_data'] =
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectCreate(CreateView):
    model = Project
    template_name = 'apps/projects/project_form.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Create Project',
            'title': 'Create Project',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/apps/projects/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/apps/projects/dashboard.js'
            ],
            'form': self.get_form_class(),
            'file_form': ProjectFileForm()
        }
        ctx = super(ProjectCreate, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        project_form = self.get_form()
        project_file_form = ProjectFileForm(request.POST, request.FILES,
                                            instance=self.object)
        files = request.FILES.getlist('file')
        if project_form.is_valid() and project_file_form.is_valid():
            self.object = project_form.save()
            for f in files:
                project_file_instance = File(file=f, project=self.object)
                project_file_instance.save()
            super(ProjectCreate, self).form_valid(project_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)


class ProjectEdit(UpdateView):
    model = Project
    template_name = 'apps/projects/project_form.html'
    form_class = ProjectForm

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)

    def get_success_url(self):
        return reverse('summit.apps.projects:project-detail', args=[str(self.object.id)])

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Edit Project',
            'title': 'Edit Project',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/apps/projects/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/apps/projects/dashboard.js'
            ],
            'files': File.objects.filter(project=self.object),
            'file_form': ProjectFileForm()
        }
        ctx = super(ProjectEdit, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        project_form = self.get_form()
        project_file_form = ProjectFileForm(request.POST, request.FILES,
                                            instance=self.object)
        files = request.FILES.getlist('file')
        if project_form.is_valid() and project_file_form.is_valid():
            self.object = project_form.save()
            for f in files:
                project_file_instance = File(file=f, project=self.object)
                project_file_instance.save()
            super(ProjectEdit, self).form_valid(project_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        super(ProjectEdit, self).post(request)
        return HttpResponseRedirect(self.get_success_url())


class ProjectModifications(UpdateView):
    template_name = 'apps/projects/project_options.html'
    model = Project
    form_class = ProjectForm

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


def export_to_csv(request, id):
    project = Project.objects.get(pk=id)
    if project is None:
        return Http404("Project does not exist.")
    file_name = project.project_title

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+file_name+'.csv"'

    writer = csv.writer(response)
    writer.writerow(['project_title', 'status', 'budget', 'student_support', 'short_summary'])

    writer.writerow([project.project_title, project.status, project.budget, project.student_support, project.short_summary])

    return response


def change_history(request, id):
    return HttpResponseRedirect(reverse('admin:summit_projects_project_history', args=id))
