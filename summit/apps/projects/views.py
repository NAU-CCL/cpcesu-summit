import csv
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from summit.libs.auth.models import UserProfile, CESUnit

from .models import Project, File, Location, Modification, ModFile
from .forms import ProjectForm, ProjectFileForm, LocationForm, ModificationForm, ModificationFileForm


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
        all_projects = self.get_queryset()

        user = self.request.user
        user_group = self.request.user.group

        try:
            profile = UserProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            profile = None

        try:
            ces_unit = CESUnit.objects.get(id=user_group.id)
        except (ObjectDoesNotExist, AttributeError) as e:
            ces_unit = None

        user_filtered_projects = all_projects.filter(cesu_unit=ces_unit, staff_member=profile) \
                                 | all_projects.filter(cesu_unit=None) \
                                 | all_projects.filter(staff_member=profile)

        start_date = datetime.datetime.now() + datetime.timedelta(-30)
        recent_projects = all_projects.filter(date__range=[start_date, datetime.datetime.now()])
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
            ],
            'projects': user_filtered_projects,
            'recent_projects': recent_projects
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
    confirm_status = False

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
            'file_form': ProjectFileForm(),
            'confirm_status': self.confirm_status
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


class ProjectEdit(UpdateView):
    model = Project
    template_name = 'apps/projects/project_edit_form.html'
    form_class = ProjectForm
    status = False

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


class ProjectModifications(CreateView):
    template_name = 'apps/projects/project_modifications.html'
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
    writer.writerow(['Budget', 'CESUnit', 'Description', 'Discipline', 'Federal Agency', 'Field of Science',
                     'Final Report ', 'Fiscal Year', 'Initial Start Date', 'Location',
                     'Monitoring', 'Project Notes', 'Number of Students', 'P-Num', 'Partner', 'Principal Investigator (PI)',
                     'Project Manager','Project Title', 'Research & Development', 'Scientific Method', 'Sensitive',
                     'Short Summary', 'Source of Funding', 'Staff Member',
                     'Status', 'Student Support', 'Technical Representative', 'Tentative End Date',
                     'Tentative Start Date', 'Type of Project', 'Veteran/Youth Support'])

    writer.writerow([project.budget, project.cesu_unit,project.description, project.discipline, project.federal_agency,
                     project.field_of_science, project.final_report, project.fiscal_year, project.init_start_date,
                     project.location, project.monitoring, project.notes, project.num_of_students, project.p_num,
                     project.partner, project.pp_i, project.project_manager, project.project_title, project.r_d,
                     project.sci_method, project.sensitive, project.short_summary, project.src_of_funding,
                     project.staff_member, project.status, project.student_support, project.tech_rep, project.tent_end_date,
                     project.tent_start_date, project.type, project.vet_support])

    return response


def change_history(request, id):
    return HttpResponseRedirect(reverse('admin:summit_projects_project_history', args=id))
