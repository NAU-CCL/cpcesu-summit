import csv
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse

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
from .choices import ProjectChoices


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'apps/projects/project_all_fields.html'
    model = Project
    context_object_name = 'projects'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    raise_exception = False

    def get_context_data(self, **kwargs):
        all_projects = Project.objects.all()

        projects = []

        for proj in all_projects:
            modifications = Modification.objects.filter(project=proj)
            total_mod_amount = 0
            for mod in modifications:
                total_mod_amount += mod.mod_amount
            proj.total_award_amount = (proj.budget or 0) + total_mod_amount
            projects.append(proj)

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
            'table2_disabled': True,
            'projects': projects
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
        projects = Project.objects.exclude(status="DRAFT").exclude(status="").exclude(status="LEGACY")
        return projects

    def get_context_data(self, **kwargs):
        context = {
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

        # If widget vs. full website
        if "name" in self.kwargs and self.kwargs['name'] is not None:
            context['name'] = self.kwargs['name']
        if "is_widget" in self.kwargs and self.kwargs['is_widget'] is True:
            context['my_template'] = 'layouts/widget.html'
            context['link_target'] = '_blank'
            context['is_widget'] = True
        else:
            context['my_template'] = 'layouts/base.html'

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
        all_projects = Project.objects.only("id")
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
                                 | all_projects.filter(staff_member=None, status="DRAFT")

        dashboard_projects = []

        for proj in user_filtered_projects:
            modifications = Modification.objects.filter(project=proj)
            total_mod_amount = 0
            for mod in modifications:
                total_mod_amount += mod.mod_amount
            proj.total_award_amount = (proj.budget or 0) + total_mod_amount
            dashboard_projects.append(proj)



        context = {
            'name': self.kwargs['name'],
            'pagetitle': 'Project Dashboard',
            'table1_header': 'Project Search',
            'table1_desc': 'A table to be filled with projects matching your search criteria',
            'table2_header': 'All Recent Projects',
            'table2_desc': 'A table of all of the projects that have been created in the last 30 days',
            'title': 'Project Dashboard',
            'bannerTemplate': 'none',
            'header': {},
            'cssFiles': [
                'libs/mdb/css/addons/datatables.min.css',
                'css/datatables/dashboard.css'
            ],
            'jsFiles': [
                'libs/mdb/js/addons/datatables.min.js',
                'js/datatables/dashboard.js',
                'js/apps/projects/filter.js',
                'js/apps/projects/search.js'
            ],
            'projects': all_projects,
        }
        ctx = super(ProjectDashboardView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

    # TODO: integrate this get_obkect into context
    def get_object(self, **kwargs):
        pk_ = self.kwargs.get("id")
        return get_object_or_404(Project, pk=pk_)


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

    def update_extension(self):
        time_ext1 = ProjectChoices.MOD_TYPE[2][0]
        time_ext2 = ProjectChoices.MOD_TYPE[4][0]
        time_ext3 = ProjectChoices.MOD_TYPE[6][0]
        prj = self.get_object()
        modifications = Modification.objects.filter(project=prj).order_by('-pk')
        for mod in modifications:
            mod_type = mod.mod_type
            if mod_type == time_ext1 or mod_type == time_ext2 or mod_type == time_ext3:
                return mod.mod_extension

        modifications1 = Modification.objects.filter(mod_type__contains='Time Extension')
        return modifications1

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
                'js/datatables/dashboard.js',
                'js/apps/projects/editProject.js'

            ],
            'total_award_amount': self.total_award_amount(),
            'date_ext': self.update_extension()

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
            try:
                profile = UserProfile.objects.get(user=request.user)
                form = ProjectForm(initial={'staff_member': profile})
            except ObjectDoesNotExist:
                pass

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
                'form': form,
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
        proj = self.get_object()
        form = ProjectForm(instance=proj, initial={
            "federal_agency": proj.federal_agency,
            "partner": proj.partner,
            "location": proj.location,

            "project_manager": proj.project_manager,
            "tech_rep": proj.tech_rep,
            "pp_i": proj.pp_i,
            "staff_member": proj.staff_member
        })
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
            'federal_agency': self.get_object().federal_agency,
            'form': form
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
    federal_agency = project_form.cleaned_data['federal_agency']
    if federal_agency and len(federal_agency) > 0:
        try:
            federal_agency = FederalAgency.objects.get(name=federal_agency)
        except ObjectDoesNotExist:
            federal_agency = FederalAgency(name=federal_agency)
            federal_agency.save()
    else:
        federal_agency = None
    project_form.instance.federal_agency = federal_agency

    # Partner
    partner = project_form.cleaned_data['partner']
    if partner and len(partner) > 0:
        try:
            partner = Partner.objects.get(name=partner)
        except ObjectDoesNotExist:
            partner = Partner(name=partner)
            partner.save()
    else:
        partner = None
    project_form.instance.partner = partner

    # Location
    location = project_form.cleaned_data['location']
    if location and len(location) > 0:
        name_parts = location.split(" ")
        if len(name_parts) >= 2:
            name = ' '.join(name_parts[:-1])
            abrev = name_parts[-1].strip('()')
            print(name, abrev)
            try:
                location = Location.objects.get(name=name)
            except ObjectDoesNotExist:
                location = Location(name=name, abbrv=abrev)
                location.save()
    else:
        location = None
    project_form.instance.location = location

    # CES Unit
    cesu = CESUnit.objects.get(pk=1)
    project_form.instance.cesu_unit = cesu

    # Project Manager
    project_manager = project_form.cleaned_data['project_manager']
    if project_manager and len(project_manager) > 0:
        # First split based on space
        name_parts = project_manager.split(" ")
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
            project_manager = None

            try:
                # Second map and save
                # project_form.instance.project_manager
                project_managers = UserProfile.objects.filter(first_name=first_name, last_name=last_name)

                if project_managers is None:
                    raise ObjectDoesNotExist("No project_managers exist with that query")

                for f_project_manager in project_managers:
                    # If in assigned group
                    if (f_project_manager.assigned_group and federal_agency and f_project_manager.assigned_group.id == federal_agency.id) \
                            or (f_project_manager.assigned_group and cesu and f_project_manager.assigned_group.id == cesu.id):
                        project_manager = f_project_manager
                        break

                if project_manager is None:
                    project_manager = project_managers.first()

                if project_manager is None:
                    raise ObjectDoesNotExist("No federal managers exists with that query")

            except ObjectDoesNotExist:
                project_manager = UserProfile(first_name=first_name, last_name=last_name, assigned_group=federal_agency)
                project_manager.save()
    else:
        project_manager = None
    project_form.instance.project_manager = project_manager

    # Tech Rep
    tech_rep = project_form.cleaned_data['tech_rep']
    if tech_rep and len(tech_rep) > 0:
        # First split based on space
        name_parts = tech_rep.split(" ")
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
            tech_rep = None

            try:
                # Second map and save
                # project_form.instance.project_manager
                tech_reps = UserProfile.objects.filter(first_name=first_name, last_name=last_name)

                if tech_reps is None:
                    raise ObjectDoesNotExist("No tech_reps exist with that query")

                for f_tech_rep in tech_reps:
                    # If in assigned group
                    if (
                            f_tech_rep.assigned_group and federal_agency and f_tech_rep.assigned_group.id == federal_agency.id) \
                            or (
                            f_tech_rep.assigned_group and cesu and f_tech_rep.assigned_group.id == cesu.id):
                        tech_rep = f_tech_rep
                        break

                if tech_rep is None:
                    tech_rep = tech_reps.first()

                if tech_rep is None:
                    raise ObjectDoesNotExist("No tech_rep exists with that query")

            except ObjectDoesNotExist:
                tech_rep = UserProfile(first_name=first_name, last_name=last_name,
                                                  assigned_group=federal_agency)
                tech_rep.save()
    else:
        tech_rep = None
    project_form.instance.tech_rep = tech_rep

    # Partner principle investigator
    pp_i = project_form.cleaned_data['pp_i']
    if pp_i and len(pp_i) > 0:
        # First split based on space
        name_parts = pp_i.split(" ")
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
            pp_i = None

            try:
                # Second map and save
                # project_form.instance.project_manager
                pp_is = UserProfile.objects.filter(first_name=first_name, last_name=last_name)

                if pp_is is None:
                    raise ObjectDoesNotExist("No pp_is exist with that query")

                for f_pp_i in pp_is:
                    # If in assigned group
                    if (
                            f_pp_i.assigned_group and partner and f_pp_i.assigned_group.id == partner.id) \
                            or (
                            f_pp_i.assigned_group and cesu and f_pp_i.assigned_group.id == cesu.id):
                        pp_i = f_pp_i
                        break

                if pp_i is None:
                    pp_i = pp_is.first()

                if pp_i is None:
                    raise ObjectDoesNotExist("No pp_i exists with that query")

            except ObjectDoesNotExist:
                pp_i = UserProfile(first_name=first_name, last_name=last_name,
                                       assigned_group=partner)
                pp_i.save()
    else:
        pp_i = None
    project_form.instance.pp_i = pp_i

    # CESU Staff Member
    staff_member = project_form.cleaned_data['staff_member']
    if staff_member and len(staff_member) > 0:
        # First split based on space
        name_parts = staff_member.split(" ")
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
            staff_member = None

            try:
                # Second map and save
                # project_form.instance.project_manager
                staff_members = UserProfile.objects.filter(first_name=first_name, last_name=last_name)

                if staff_members is None:
                    raise ObjectDoesNotExist("No staff_members exist with that query")

                for f_staff_member in staff_members:
                    # If in assigned group
                    if f_staff_member.assigned_group and cesu and f_staff_member.assigned_group.id == cesu.id:
                        staff_member = f_staff_member
                        break

                if staff_member is None:
                    staff_member = staff_members.first()

                if staff_member is None:
                    raise ObjectDoesNotExist("No staff_member exists with that query")

            except ObjectDoesNotExist:
                staff_member = UserProfile(first_name=first_name, last_name=last_name,
                                   assigned_group=cesu)
                staff_member.save()
    else:
        staff_member = None
    project_form.instance.staff_member = staff_member

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

    def total_award_amount(self):
        prj = get_object_or_404(Project, pk=self.kwargs.get("id"))
        modifications = Modification.objects.filter(project=prj)
        total_mod_amount = 0
        for mod in modifications:
            total_mod_amount += mod.mod_amount
        return (prj.budget or 0) + total_mod_amount

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
            'file_form': ModificationFileForm(),
            'total_award_amount': self.total_award_amount()
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

    def total_award_amount(self):
        prj = get_object_or_404(Project, pk=self.kwargs.get("id"))
        modifications = Modification.objects.filter(project=prj)
        total_mod_amount = 0
        for mod in modifications:
            total_mod_amount += mod.mod_amount
        return (prj.budget or 0) + total_mod_amount

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
            'file_form': ModificationFileForm(),
            'total_award_amount': self.total_award_amount()
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
from config.settings.shared import DEFAULT_FROM_EMAIL


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

            recipients = [DEFAULT_FROM_EMAIL, ]
            if cc_myself:
                cust_emails = [recipients[0], customer_email]
                message = get_template('apps/projects/partials/project_request_public.html').render(ctx)
                email = EmailMessage(subject, message, to=cust_emails)
                email.content_subtype = "html"
                email.send()

            message = get_template('apps/projects/partials/project_request_email.html').render(ctx)
            email = EmailMessage(subject, message, to=recipients)
            email.content_subtype = "html"
            email.send()

            return HttpResponseRedirect(reverse('summit.apps.projects:project_public_detail', kwargs={"id": project_id}))

    else:
        form = ContactForm(initial={'project_id': project_id})

    return render(request, template_name, {'form': form, 'project': project})


from rest_framework import viewsets
from .serializers import FederalAgencySerializer, PartnerSerializer, LocationSerializer, UserProfileSerializer


class FederalAgencyViewSet(viewsets.ModelViewSet):
    queryset = FederalAgency.objects.all().order_by('name')
    serializer_class = FederalAgencySerializer
    http_method_names = ['get']
    pagination_class = None


class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all().order_by('name')
    serializer_class = PartnerSerializer
    http_method_names = ['get']
    pagination_class = None


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('name')
    serializer_class = LocationSerializer
    http_method_names = ['get']
    pagination_class = None


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('last_name')
    serializer_class = UserProfileSerializer
    http_method_names = ['get']
    pagination_class = None

    def get_queryset(self):
        queryset = UserProfile.objects.all().order_by('last_name')
        group_id = self.request.query_params.get('assigned_group_pk', None)
        group_name = self.request.query_params.get('assigned_group_name', None)

        if group_id is not None:
            queryset = queryset.filter(assigned_group_id=group_id)
        elif group_name is not None:
            try:
                group = UserGroup.objects.get(name=group_name)
                queryset = queryset.filter(assigned_group=group)
            except ObjectDoesNotExist:
                queryset = UserProfile.objects.none()

        return queryset

#
#
# Other, non-view supporting functions
#
#


def export_to_csv(request):
    time_ext1 = ProjectChoices.MOD_TYPE[2][0]
    time_ext2 = ProjectChoices.MOD_TYPE[4][0]
    time_ext3 = ProjectChoices.MOD_TYPE[6][0]

    file_name = "multi_project_export"
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '.csv"'

    writer = csv.writer(response)
    writer.writerow(['FY', 'Agency', 'Award #', 'Awarding Office', 'Partner', 'Place', 'Title', 'Type', 'Discipline',
                     'Youth/Vets', 'Agency Project Manager', 'Agency Agreements Technical Representative',
                     'Partner Principle Investigator', 'Received', 'Reviewed', 'Approved', 'Executed', 'Start', 'End',
                     'Extension', 'Description/Abstract', 'Initial', 'Total Award Amount', 'Funding Source',
                     'Monitoring', 'Scientific Method', 'Field', 'Subfield', 'Status,', 'Sensitive',
                     'Deliverable(s) Received', 'Notes'])

    if request.POST:
        export_list = request.POST.getlist("export_list")

        if len(export_list) <= 0:
            return HttpResponse('')

        for project_id in export_list:
            project = Project.objects.get(pk=project_id)
            modifications = Modification.objects.filter(project=project)
            total_mod_amount = 0

            # Finding Total Award Amount
            for mod in modifications:
                total_mod_amount += mod.mod_amount
            total_award_amount = (project.budget or 0) + total_mod_amount

            # Finding the most recent extended date
            ext_mods = Modification.objects.filter(project=project).order_by('-pk')
            ext_date = None
            for mod in ext_mods:
                mod_type = mod.mod_type
                if mod_type == time_ext1 or mod_type == time_ext2 or mod_type == time_ext3:
                    ext_date = mod.mod_extension
                    break

            if project is None:
                continue

            writer.writerow(
                [project.fiscal_year, project.federal_agency, project.p_num, project.award_office, project.partner,
                 project.location, project.project_title, project.type, project.discipline, project.youth_vets,
                 project.project_manager, project.tech_rep, project.pp_i, project.init_start_date, project.reviewed,
                 project.task_agreement_start_date, project.exec_start_date, project.tent_start_date,
                 project.tent_end_date, ext_date, project.description, project.budget, total_award_amount,
                 project.src_of_funding, project.monitoring, project.sci_method, project.field_of_science,
                 project.field_of_science_sub, project.status, project.sensitive, project.final_report, project.notes])

    return response

def project_filter(request):
    if request.is_ajax():
        print(request.GET)
        start = int(request.GET.get('start_date'))
        end = int(request.GET.get('end_date'))
        desiredstatus = request.GET.get('status')
        partners = Partner.objects.all().values()
        agencies = FederalAgency.objects.all().values()
        projects = Project.objects.only("project_id", "status", "federal_agency", "partner", "fiscal_year", "p_num",
                                        "project_title", "total_award_amount", "tent_start_date", "tent_end_date",
                                        "project_manager", "pp_i")
        projects = projects.filter(fiscal_year__range=[start, end], status=desiredstatus.upper()).values()
        managers = UserProfile.objects.all().values()
        return JsonResponse({'projects': list(projects), 'agencies': list(agencies), 'partners': list(partners),
                             'managers': list(managers)})

    projects = Project.objects.filter()
    return JsonResponse({'projects': list(projects)})


def project_search(request):
    if request.is_ajax():
        FY = request.GET.get('FY')
        print(FY)
        Partner_name = request.GET.get('partner_name')
        Partner_name.strip()
        AwardNum = request.GET.get('AwardNumber')
        AwardNum.strip()
        partners = Partner.objects.all().values()
        agencies = FederalAgency.objects.all().values()
        projects = Project.objects.only("project_id", "status", "federal_agency", "partner", "fiscal_year", "p_num",
                                        "project_title", "total_award_amount", "tent_start_date", "tent_end_date",
                                        "project_manager", "pp_i")

        partner_ids = Partner.objects.filter(name__contains=Partner_name).values_list("id", flat=True)
        agency_ids= FederalAgency.objects.filter(name__contains=Partner_name).values_list("id", flat=True)
        if(FY != ""):
            projects = projects.filter(fiscal_year__contains=FY)
        if (AwardNum != ""):
            projects = projects.filter(p_num__contains=AwardNum)
        if (Partner_name != ""):
            projects = projects.filter(partner_id__in=partner_ids) | projects.filter(federal_agency_id__in=agency_ids)
            partners = partners.filter(name__contains = Partner_name)

        projects = projects.values()
        managers = UserProfile.objects.all().values()
        return JsonResponse({'projects': list(projects), 'agencies': list(agencies), 'partners': list(partners),
                             'managers': list(managers)})

    projects = Project.objects.filter()
    return JsonResponse({'projects': list(projects)})

