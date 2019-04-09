import csv
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files import File

from celery.result import AsyncResult
import json

from .models import Project, File
from .forms import ProjectForm, ProjectFileForm
from .tasks import read_pdf


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
            'header': {
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
            'pagetitle': 'Projects Details',
            'title': 'Projects Details',
            'header': {
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
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectCreate(CreateView):
    model = Project
    template_name = 'apps/projects/project_form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        project = form.save()
        read_pdf.delay(project.file.path)
        return super(ProjectCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('summit.apps.projects:project-detail', args=[str(self.object.id)])

    def get(self, request, *args, **kwargs):
        if 'job' in request.GET:
            job_id = request.GET['job']
            project = Project.objects.get(job_id=job_id)
            form = self.form_class(instance=project)
            #upload = File.objects.filter()[:1].get()
            #print(str(upload.file.path))

            return render(request, self.template_name, {'form': form,})#'file_path': upload.file.path})
        else:
            form = self.form_class
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        print('over there 1')
        context = {
            'name': 'Create',
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
        self.object = self.get_object()
        project_form = ProjectForm(request.POST)
        project_file_form = ProjectFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if project_form.is_valid() and project_file_form.is_valid():
            self.form_valid(project_form, project_file_form, files)
        else:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return super(ProjectCreate, self).post(request)

    def form_valid(self, project_form, project_file_form, files):
        self.object = project_form.save()
        for f in files:
            project_file_instance = File(file=f, project=self.object)
            project_file_instance.save()
        return super(ProjectCreate, self).form_valid(project_form)


class ProjectEdit(UpdateView):
    template_name = 'apps/projects/project_form.html'
    model = Project
    form_class = ProjectForm

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


def project_form_redirect(request, name):
    template_name = 'apps/projects/project_form_redirection.html'

    context = {
        'name': name,
        'pagetitle': 'not Home',
        'title': 'Form rediceiction, autofill or manual',
        'bannerTemplate': 'fullscreen',
        'header': {
            'heading1': 'Project Creation Redirection',
            'heading2': '',
            'buttons': [
                {
                    'name': 'Autofill',
                    'link': '/projects/autofill'
                },
                {
                    'name': 'Manual',
                    'link': '/projects/create',
                }
            ]
        },
    }
    return render(request, template_name, context)


class ProjectAutofill(View):
    form_class = ProjectFileForm
    success_url = reverse_lazy('summit.apps.projects:project-create')
    template_name = 'apps/projects/autofill_form.html'

    def get(self, request):
        form = self.form_class()
        if 'job' in request.GET:
            job_id = request.GET['job']
            job = AsyncResult(job_id)
            data = job.result or job.state
            context = {
                'data': data,
                'task_id': job_id,
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            job = read_pdf.delay(upload.file.path)
            print(upload.file.path)
            return HttpResponseRedirect(reverse('projects:project-progress') + '?job=' + job.id)
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})


class ProjectProgress(UpdateView):
    template_name = 'apps/projects/progress.html'
    model = ProjectCreate

    def get(self, request, *args, **kwargs):
        print('over here\n')
        if 'job' in request.GET:
            job_id = request.GET['job']
            job = AsyncResult(job_id)
            data = job.result or job.state
            context = {
                'data': data,
                'task_id': job_id,
                'url': reverse('projects:project-create') + '?job=' + job_id,
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if 'task_id' in request.POST.keys() and request.POST['task_id']:
                task_id = request.POST['task_id']
                task = AsyncResult(task_id)
                data = task.result or task.state
            else:
                data = 'No task_id in the request'
        else:
            data = 'This is not an ajax request'

        # if data == 'SUCCESS':
        #     return HttpResponseRedirect(reverse('summit.apps.projects:project-create'))

        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')


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
    writer.writerow(['project_title', 'status', 'budget', 'student_support'])

    writer.writerow([project.project_title, project.status, project.budget, project.student_support])

    return response
