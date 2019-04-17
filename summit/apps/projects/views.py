import csv
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files import File

from celery.result import AsyncResult
import json

from .models import Project, File, Location, Modification
from .forms import ProjectForm, ProjectFileForm, LocationForm, ModificationForm
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


class ProjectPublicListView(ListView):
    template_name = 'apps/projects/project_public.html'
    model = Project
    context_object_name = 'projects'

    def get_queryset(self):
        projects = Project.objects.exclude(status="DRAFT")
        return projects

    def get_context_data(self, **kwargs):
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Public Projects List',
            'title': 'Public Projects List',
            'header': {
            },
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/apps/projects/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/apps/projects/dashboard.js'
            ],
            'project_url': 'summit.apps.projects:project-detail-public'
        }
        ctx = super(ProjectPublicListView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    # TODO: integrate this get_obkect into context
    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectDashboardView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'apps/projects/project_index.html'
    model = Project
    context_object_name = 'projects'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Your Dashboard',
            'title': 'Your Dashboard',
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
        ctx = super(ProjectDashboardView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    # TODO: integrate this get_obkect into context
    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


# TODO: Change context object name
class ProjectDetail(LoginRequiredMixin, DetailView):
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
        ctx['files'] = File.objects.filter(project=self.object)
        ctx['mods'] = Modification.objects.filter(project=self.object)
        # ctx['history_data'] =
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectPublicDetail(DetailView):
    model = Project
    template_name = 'apps/projects/project_detail_public.html'

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
        ctx = super(ProjectPublicDetail, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        # ctx['history_data'] =
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectCreate(CreateView):
    model = Project
    template_name = 'apps/projects/project_create_form.html'
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
            return render(request, self.template_name, context)

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
        project_form = ProjectForm(request.POST, request.FILES, instance=self.object)
        project_file_form = ProjectFileForm(request.POST, request.FILES,
                                            instance=self.object)
        files = request.FILES.getlist('file')
        if project_form.is_valid():
            self.object = project_form.save()
            if project_file_form.is_valid():
                for f in files:
                    project_file_instance = File(file=f, project=self.object)
                    project_file_instance.save()
            super(ProjectCreate, self).form_valid(project_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            print(project_form.errors)
            ctx = self.get_context_data()
            ctx['form'] = project_form
            ctx['file_form'] = project_file_form
            return self.render_to_response(ctx)


class ProjectEdit(UpdateView):
    model = Project
    template_name = 'apps/projects/project_edit_form.html'
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


class ProjectModifications(CreateView):
    template_name = 'apps/projects/project_options.html'
    model = Modification
    form_class = ModificationForm

    def get_success_url(self):
        return reverse('summit.apps.projects:project-detail',
                       args=[self.kwargs.get("id")])

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Project Modifications',
            'title': 'Project Modifications',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/apps/projects/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/apps/projects/dashboard.js'
            ],
            'project': get_object_or_404(Project, pk=self.kwargs.get("id"))
        }
        ctx = super(ProjectModifications, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
            self.object = None
            mod_form = self.get_form()
            mod_form.instance.project = get_object_or_404(Project, pk=self.kwargs.get("id"))
            if mod_form.is_valid():
                self.object = mod_form
                mod_form.instance.project = get_object_or_404(Project, pk=self.kwargs.get("id"))
                super(ProjectModifications, self).form_valid(mod_form)
                return HttpResponseRedirect(self.get_success_url())
            else:
                ctx = self.get_context_data()
                ctx['form'] = mod_form
                return self.render_to_response(ctx)


class ProjectModEdit(UpdateView):
    model = Modification
    template_name = 'apps/projects/project_options.html'
    form_class = ModificationForm

    def get_object(self, **kwargs):
        prj_ = get_object_or_404(Project, pk=self.kwargs.get("id"))
        pk_ = self.kwargs.get("mod_id")
        return Modification.objects.get(mod_num=pk_, project=prj_)

    def get_success_url(self):
        return reverse('summit.apps.projects:project-detail',
                       args=[self.kwargs.get("id")])

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Project Modifications',
            'title': 'Project Modifications',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/apps/projects/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/apps/projects/dashboard.js'
            ],
            'project': get_object_or_404(Project, pk=self.kwargs.get("id"))
        }
        ctx = super(ProjectModEdit, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            mod_form = self.get_form()
            mod_form.instance.project = get_object_or_404(Project, pk=self.kwargs.get("id"))
            if mod_form.is_valid():
                self.object = mod_form
                mod_form.instance.project = get_object_or_404(Project, pk=self.kwargs.get("id"))
                super(ProjectModEdit, self).form_valid(mod_form)
                return HttpResponseRedirect(self.get_success_url())
            else:
                ctx = self.get_context_data()
                ctx['form'] = mod_form
                return self.render_to_response(ctx)


#
#
# Location portion - single model to represent parks, states, etc. for Projects
#
#
class LocationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'apps/projects/location_list.html'
    model = Location
    context_object_name = 'locations'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Location List',
            'title': 'Location List',
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
        ctx = super(LocationListView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    # TODO: integrate this get_obkect into context
    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class LocationCreate(CreateView):
    model = Location
    template_name = 'apps/projects/location_form.html'
    form_class = LocationForm

    def get_context_data(self, **kwargs):
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Create Location',
            'title': 'Create Location',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/apps/projects/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/apps/projects/dashboard.js'
            ],
            'form': self.get_form_class(),
        }
        ctx = super(LocationCreate, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        location_form = self.get_form()
        if location_form.is_valid():
            self.object = location_form.save()
            super(LocationCreate, self).form_valid(location_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)


class LocationDetail(DetailView):
    model = Location
    template_name = 'apps/projects/location_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Location Details',
            'title': 'Location Details',
        }
        ctx = super(LocationDetail, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Location, pk=pk_)


class LocationEdit(UpdateView):
    model = Location
    template_name = 'apps/projects/location_form.html'
    form_class = LocationForm

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Location, pk=pk_)

    def get_success_url(self):
        return reverse('summit.apps.projects:location-detail', args=[str(self.object.id)])

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Edit Location',
            'title': 'Edit Location'
        }
        ctx = super(LocationEdit, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        location_form = self.get_form()

        if location_form.is_valid():
            self.object = location_form.save()
            super(LocationEdit, self).form_valid(location_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)

#
#
# Other, non-view supporting functions
#
#


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
