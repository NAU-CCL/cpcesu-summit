import csv
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse

from celery.result import AsyncResult
import json

from .models import Project, Notification, ProjectFiles
from .forms import ProjectForm, ProjectFilesForm
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
            # 'bannerTemplate': 'fullscreen',
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
        # ctx['history_data'] =
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


# class ProjectCreate(CreateView):
#     template_name = 'apps/projects/project_form.html'
#     model = Project
#     form_class = ProjectForm

class ProjectCreate(CreateView):
    model = Project
    template_name = 'apps/projects/project_form.html'
    form_class = ProjectForm

    def form_valid(self, form):
        proj = form.save()
        print(proj.project_title)
        read_pdf.delay(proj.file.path)
        return super(ProjectCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('summit.apps.projects:project-detail', args=[str(self.object.id)])

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


class ProjectAutofill(CreateView):
    template_name = 'apps/projects/autofill_form.html'
    model = ProjectFiles
    form_class = ProjectFilesForm

    def form_valid(self, form):
        upload = form.save()
        job = read_pdf.delay(upload.file.path)
        return HttpResponseRedirect(reverse('projects:project-autofill') + '?job=' + job.id)

    def get(self, request, *args, **kwargs):
        if 'job' in request.GET:
            job_id = request.GET['job']
            job = AsyncResult(job_id)
            data = job.result or job.state
            context = {
                'data': data,
                'task_id': job_id,
            }
            return render(request, "apps/projects/autofill_form.html", context)
        else:
            form = ProjectFilesForm()
            context = {
                'form': form,
            }
            return render(request, "apps/projects/autofill_form.html", context)


def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

#
# def autofill(request):
#     form = ProjectFilesForm(request.POST)
#
#     if 'job' in request.GET:
#         job_id = request.GET['job']
#         job = AsyncResult(job_id)
#         data = job.result or job.state
#         context = {
#             'data': data,
#             'task_id': job_id,
#         }
#         return render(request, "apps/projects/autofill_form.html", context)
#     elif request.method == 'POST' and form.is_valid():
#         upload = form.save()
#         job = read_pdf.delay(upload.file.path)
#         return HttpResponseRedirect(reverse('/projects/autofill') + '?job=' + job.id)
#     else:
#         form = ProjectFilesForm()
#         context = {
#             'form': form,
#         }
#         return render(request, "apps/projects/autofill_form.html", context)


"""
class ProgressHandler:

    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, 'X-Progress-ID'
    which should contain a unique string to identify the upload to be tracked.
    

    def __init__(self, delay, request):
        self.request = request
        self.progress_id = None
        self.delay = delay


# A view to report back on upload progress:

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError


def upload_progress(request):
    
    Return JSON object with information about the progress of an upload.
    
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        from django.utils import simplejson
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        return HttpResponse(simplejson.dumps(data))
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')
"""

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
