from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse

from celery.result import AsyncResult
import json

from .models import Project, Notification, ProjectFiles
from .forms import ProjectForm, ProjectFilesForm
from .tasks import read_pdf


# def index(request):
#     template_name = 'apps/projects/project_index.html'
#
#     return render(request, template_name, context)
#
# # TODO: Refactor ProjectList() to display projects in order by status.


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'apps/projects/project_index.html'
    model = Project
    context_object_name = 'projects'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Home',
            'title': 'Home page',
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

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectCreate(CreateView):
    template_name = 'apps/projects/project_form.html'
    model = Project
    form_class = ProjectForm

    # def upload_view(self, request):
    #     if request.method == 'POST':
    #         form = ProjectForm(data = request.POST, files=request.FILES)
    #         if form.is_valid():
    #             print('Valid form')
    #         else:
    #             print('Invalid form')

    def form_valid(self, form):
        proj = form.save()
        print(proj.project_title)
        read_pdf.delay(proj.file.path)
        return super(ProjectCreate, self).form_valid(form)

    """def create_project(self, request):
        if request.method == 'POST':
            post_text = request.POST.get('the_post')
            response_data = {}

            post = Project(text=post_text, author=request.user)
            post.save()

            response_data['result'] = 'Create post successful!'
            response_data['postpk'] = post.pk
            response_data['text'] = post.text
            response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
            response_data['author'] = post.author.username

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )"""


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



