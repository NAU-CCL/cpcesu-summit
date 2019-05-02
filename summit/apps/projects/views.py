import csv
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files import File

from celery.result import AsyncResult
import json

from .tasks import read_pdf
from summit.libs.auth.models import UserProfile, CESUnit, FederalAgency, Partner, UserGroup
from .models import Project, File, Location, Modification, ModFile
from .forms import ProjectForm, ProjectFileForm, LocationForm, ModificationForm, ModificationFileForm, ContactForm


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
            'pagetitle': 'All Projects List',
            'table1_header': " ",
            'table1_desc': "A table of every project in the system",
            'title': 'Projects List',
            'bannerTemplate': 'none',
            'header': {
            },
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
            ],
            'table2_disabled': True
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
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
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
        all_projects = self.get_queryset()

        user = self.request.user

        try:
            profile = UserProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            profile = None

        if profile is not None:
            try:
                ces_unit = CESUnit.objects.get(id=profile.assigned_group.id)
            except (ObjectDoesNotExist, AttributeError) as e:
                ces_unit = None
        else: ces_unit = None

        user_filtered_projects = all_projects.filter(cesu_unit=ces_unit, staff_member=profile, status="DRAFT") \
                                 | all_projects.filter(cesu_unit=None, status="DRAFT") \
                                 | all_projects.filter(staff_member=profile, status="DRAFT")

        start_date = datetime.datetime.now() + datetime.timedelta(-30)
        recent_projects = all_projects.filter(created_on__range=[start_date, datetime.datetime.now()])
        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Your Dashboard',
            'table1_header': 'Your Assigned Projects',
            'table1_desc': 'A table of all projects in the drafting stage, either assigned to you or unassigned.',
            'table2_header': 'All Recent Projects',
            'table2_desc': 'A table of all of the projects that have been created in the last 30 days',
            'title': 'Your Dashboard',
            'bannerTemplate': 'none',
            'header': {},
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
            ],
            'projects': user_filtered_projects,
            'recent_projects': recent_projects,
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

    def total_award_amount(self):
        prj = self.get_object()
        modifications = Modification.objects.filter(project=prj)
        total_mod_amount = 0
        for mod in modifications:
            total_mod_amount += mod.mod_amount
        return (prj.budget or 0) + total_mod_amount

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Projects Details',
            'title': 'Projects Details',
            'bannerTemplate': 'none',
            'header': {
            },
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
            ],
            'total_award_amount': self.total_award_amount()

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

    def total_award_amount(self):
        prj = self.get_object()
        modifications = Modification.objects.filter(project=prj)
        total_mod_amount = 0
        for mod in modifications:
            total_mod_amount += mod.mod_amount
        return (prj.budget or 0) + total_mod_amount

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Projects Details',
            'title': 'Projects Details',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
            ],
            'total_award_amount': self.total_award_amount()
        }
        ctx = super(ProjectPublicDetail, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


class ProjectCreate(CreateView):
    model = Project
    template_name = 'apps/projects/project_create_form.html'
    form_class = ProjectForm
    confirm_status = False

    def form_valid(self, form):
        project = form.save()
        read_pdf.delay(project.file.path)
        return super(ProjectCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('summit.apps.projects:project_detail', args=[str(self.object.id)])

    def get(self, request, *args, **kwargs):
        if 'job' in request.GET:
            job_id = request.GET['job']
            project = Project.objects.get(job_id=job_id)
            form = self.form_class(instance=project)

            return render(request, self.template_name, {'form': form})
        else:
            context = {
                'name': self.kwargs['name'],
                'pagetitle': 'Create Project',
                'title': 'Create Project',
                'bannerTemplate': 'none',
                'cssFiles': [
                    'css/apps/projects/autofill.css',
                ],
                'jsFiles': [
                    'js/apps/projects/autocomplete.js',
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
            'bannerTemplate': 'none',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
            ],
            'form': self.get_form(),
            'file_form': ProjectFileForm(),
            'confirm_status': self.confirm_status
        }
        ctx = super(ProjectCreate, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        project = get_object_or_404(Project, pk=pk_)
        print(kwargs)
        return project

    def post(self, request, *args, **kwargs):
        self.object = None
        project_form = ProjectForm(request.POST, request.FILES, instance=self.object)
        project_file_form = ProjectFileForm(request.POST, request.FILES,
                                            instance=self.object)
        files = request.FILES.getlist('file')
        if project_form.is_valid():
            project_form = check_fields(project_form)

            self.object = project_form.save()
            if self.object.status != 'DRAFT':
                self.confirm_status = True
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
        super(ProjectCreate, self).post(request)
        return HttpResponseRedirect(self.get_success_url())


class ProjectEdit(UpdateView):
    model = Project
    template_name = 'apps/projects/project_edit_form.html'
    form_class = ProjectForm
    status = False

    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)

    def total_award_amount(self):
        prj = self.get_object()
        modifications = Modification.objects.filter(project=prj)
        total_mod_amount = 0
        for mod in modifications:
            total_mod_amount += mod.mod_amount
        return (prj.budget or 0) + total_mod_amount

    def get_success_url(self):
        return reverse('summit.apps.projects:project_detail', args=[str(self.object.id)])

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Edit Project',
            'title': 'Edit Project',
            'bannerTemplate': 'none',
            'cssFiles': [
                'css/apps/projects/autofill.css',
            ],
            'jsFiles': [
                'js/apps/projects/autocomplete.js',
            ],
            'files': File.objects.filter(project=self.object),
            'file_form': ProjectFileForm(),
            'total_award_amount': self.total_award_amount(),
            'federal_agency': self.get_object().federal_agency

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
            project_form = check_fields(project_form)
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


def check_fields(project_form):
    # Federal Agency
    fed_agency = project_form.cleaned_data['federal_agency']
    if fed_agency and len(fed_agency) > 0:
        try:
            project_form.instance.federal_agency = FederalAgency.objects.get(name=fed_agency)
        except ObjectDoesNotExist:
            print("Need to make a new one")

    # Partner
    partner = project_form.cleaned_data['partner']
    if partner and len(partner) > 0:
        try:
            project_form.instance.partner = Partner.objects.get(name=partner)
        except ObjectDoesNotExist:
            print("Need to make a new one")

    return project_form


class ProjectAutofill(View):
    form_class = ProjectFileForm
    success_url = reverse_lazy('summit.apps.projects:project-create')
    template_name = 'apps/projects/project_autofill_form.html'

    def get(self, request, name):
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
        else:
            return render(request, self.template_name, {'form': form})

    def post(self, request, name):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            job = read_pdf.delay(upload.file.path)
            print(upload.file.path)
            return HttpResponseRedirect(reverse('summit.apps.projects:project_upload_progress') + '?job=' + job.id)
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
                'url': reverse('summit.apps.projects:project_create') + '?job=' + job_id,
            }
            return render(request, self.template_name, context)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print('over there\n')
        if request.is_ajax():
            if 'task_id' in request.POST.keys() and request.POST['task_id']:
                task_id = request.POST['task_id']
                task = AsyncResult(task_id)
                data = task.result or task.state
                # print("has task id, data = ", task.result, " | state = ", task.state)
                data = json.dumps(data)
            else:
                data = 'No task_id in the request'
                # print("no task id")
        else:
            data = 'This is not an ajax request'
            # print("not ajax")

        return HttpResponse(data, content_type='application/json')


class ProjectModifications(CreateView):
    template_name = 'apps/projects/project_modifications.html'
    model = Modification
    form_class = ModificationForm

    def get_success_url(self):
        return reverse('summit.apps.projects:project_detail',
                       args=[self.kwargs.get("id")])

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Project Modifications',
            'title': 'Project Modifications',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
            ],
            'project': get_object_or_404(Project, pk=self.kwargs.get("id")),
            'files': ModFile.objects.filter(modification=self.object),
            'file_form': ModificationFileForm()
        }
        ctx = super(ProjectModifications, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        mod_form = ModificationForm(request.POST, request.FILES, instance=self.object)
        mod_form.instance.project = get_object_or_404(Project, pk=self.kwargs.get("id"))
        mod_file_form = ModificationFileForm(request.POST, request.FILES,
                                             instance=self.object)
        files = request.FILES.getlist('file')
        if mod_form.is_valid():
            self.object = mod_form.save()
            if mod_file_form.is_valid():
                for f in files:
                    mod_file_instance = ModFile(file=f, modification=self.object)
                    mod_file_instance.save()
            super(ProjectModifications, self).form_valid(mod_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            print(mod_form.errors)
            ctx = self.get_context_data()
            ctx['form'] = mod_form
            ctx['file_form'] = mod_file_form
            return self.render_to_response(ctx)


class ProjectModEdit(UpdateView):
    model = Modification
    template_name = 'apps/projects/project_modifications.html'
    form_class = ModificationForm

    def get_object(self, **kwargs):
        prj_ = get_object_or_404(Project, pk=self.kwargs.get("id"))
        pk_ = self.kwargs.get("mod_id")
        return Modification.objects.get(mod_num=pk_, project=prj_)

    def get_success_url(self):
        return reverse('summit.apps.projects:project_detail',
                       args=[self.kwargs.get("id")])

    def get_context_data(self, **kwargs):
        context = {
            'pagetitle': 'Project Modifications',
            'title': 'Project Modifications',
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
            ],
            'project': get_object_or_404(Project, pk=self.kwargs.get("id")),
            'files': ModFile.objects.filter(modification=self.object),
            'file_form': ModificationFileForm()
        }
        ctx = super(ProjectModEdit, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        mod_form = ModificationForm(request.POST, request.FILES, instance=self.object)
        mod_form.instance.project = get_object_or_404(Project, pk=self.kwargs.get("id"))
        mod_file_form = ModificationFileForm(request.POST, request.FILES,
                                             instance=self.object)
        files = request.FILES.getlist('file')
        if mod_form.is_valid():
            self.object = mod_form.save()
            if mod_file_form.is_valid():
                for f in files:
                    mod_file_instance = ModFile(file=f, modification=self.object)
                    mod_file_instance.save()
            super(ProjectModEdit, self).form_valid(mod_form)
            return HttpResponseRedirect(self.get_success_url())
        else:
            print(mod_form.errors)
            ctx = self.get_context_data()
            ctx['form'] = mod_form
            ctx['file_form'] = mod_file_form
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
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
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
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js'
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
        return reverse('summit.apps.projects:location_detail', args=[str(self.object.id)])

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
# Non-class-based views
#
#

from django.template.loader import get_template
from django.core.mail import EmailMessage


def request_project_info(request, project_id):
    template_name = 'apps/projects/project_public_request.html'

    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = "CPCESU Project Management - Project Request - " + project.project_title
            customer_email = form.cleaned_data['your_email']
            ctx = {
                "customer_name": form.cleaned_data['your_name'],
                "customer_email": customer_email,
                "message": form.cleaned_data['message'],
                "project_id": project_id,
                "request": request
            }
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['remy@nau.edu']
            if cc_myself:
                recipients.append(customer_email)

            message = get_template('apps/projects/partials/project_request_email.html').render(ctx)
            email = EmailMessage(subject, message, to=recipients, reply_to=[customer_email])
            email.content_subtype = "html"
            email.send()

            return HttpResponseRedirect(reverse('summit.apps.projects:project_public_detail', kwargs={"id": project_id}))

    else:
        form = ContactForm(initial={'project_id': project_id})

    return render(request, template_name, {'form': form, 'project': project})


from rest_framework import viewsets
from .serializers import FederalAgencySerializer, PartnerSerializer


class FederalAgencyViewSet(viewsets.ModelViewSet):
    queryset = FederalAgency.objects.all().order_by('name')
    serializer_class = FederalAgencySerializer


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by('name')
    serializer_class = PartnerSerializer

#
#
# Other, non-view supporting functions
#
#


def export_to_csv(request):
    file_name = "multi_project_export"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '.csv"'

    writer = csv.writer(response)
    writer.writerow(['Budget', 'CESUnit', 'Description', 'Discipline', 'Federal Agency', 'Field of Science',
                     'Final Report ', 'Fiscal Year', 'Initial Start Date', 'Location',
                     'Monitoring', 'Project Notes', 'Number of Students', 'P-Num', 'Partner',
                     'Principal Investigator (PI)',
                     'Project Manager', 'Project Title', 'Research & Development', 'Scientific Method', 'Sensitive',
                     'Short Summary', 'Source of Funding', 'Staff Member',
                     'Status', 'Technical Representative', 'Tentative End Date',
                     'Tentative Start Date', 'Type of Project', 'Veteran/Youth Support'])

    if request.POST:
        export_list = request.POST.getlist("export_list")

        if len(export_list) <= 0:
            return HttpResponse('')

        for project_id in export_list:
            project = Project.objects.get(pk=project_id)

            if project is None:
                continue

            writer.writerow(
                [project.budget, project.cesu_unit, project.description, project.discipline, project.federal_agency,
                 project.field_of_science, project.final_report, project.fiscal_year, project.init_start_date,
                 project.location, project.monitoring, project.notes, project.num_of_students, project.p_num,
                 project.partner, project.pp_i, project.project_manager, project.project_title, project.r_d,
                 project.sci_method, project.sensitive, project.short_summary, project.src_of_funding,
                 project.staff_member, project.status, project.tech_rep, project.tent_end_date,
                 project.tent_start_date, project.type, project.youth_vets])

    return response
