from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.db.models import Q

from .forms import ProfileForm, GroupForm, RoleForm, UserForm
from .models import User, UserProfile, UserGroup, CESUnit, FederalAgency, Partner, CESU, Organization, CESURole
from summit.apps.projects.models import Project


def request_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator

def exists_in_cesu(request):
    return CESURole.objects.filter(user_id=request.user.id, cesu_id=request.session.get('cesu')).exists()

def exists_and_is_not_viewer(request):
    print(request.user.id)
    print(CESURole.objects.filter(user_id=request.user.id, cesu_id=request.session.get('cesu')).exists())
    return CESURole.objects.get(user_id=request.user.id, cesu_id=request.session.get('cesu')).role != 'VIEWER' and CESURole.objects.filter(user_id=request.user.id, cesu_id=request.session.get('cesu')).exists()

def exists_and_is_admin(request):
    print(CESURole.objects.filter(user_id=request.user.id, cesu_id=request.session.get('cesu')).exists())
    return (CESURole.objects.get(user_id=request.user.id, cesu_id=request.session.get('cesu')).role == 'ADMIN' and CESURole.objects.filter(user_id=request.user.id, cesu_id=request.session.get('cesu')).exists()) or request.user.is_superuser


class CESUSwitcherView(LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, ListView):
   
    template_name = 'registration/cesu_selector.html'
    model = Project
    context_object_name = 'projects'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    #raise_exception = False



    def get_context_data(self, **kwargs):
        user = self.request.user
        cesu = self.request.session.get('cesu')

        print("session cesu: " + str(cesu))
        cesu_list = CESU.objects.all()

        try:
            profile = UserProfile.objects.get(user=user)
        except ObjectDoesNotExist:
            profile = None

        if profile is not None:
            try:
                profile_cesu = CESU.objects.get(id=profile.assigned_group.id)
            except (ObjectDoesNotExist, AttributeError) as e:
                profile_cesu = None
        else: profile_cesu = None

        context = {
            'cssFiles': [
                'libs/mdb/DataTables/datatables.min.css',
                'css/datatables/dashboard.css',
            ],
            'jsFiles': [
                'libs/mdb/DataTables/datatables.min.js',
                'js/libs/auth/cesu_switcher.js'
            ],
            "cesu_list": cesu_list

        }
        ctx = super(CESUSwitcherView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

def logged_out(request):
    template_name = 'registration/logged_out.html'

    context = {
        'name': 'libs.auth.logged_out',
        'pagetitle': 'Logged Out',
        'title': 'Successful Log Out',
        'bannerTemplate': 'fullscreen',
        'header': {
            'background': 'apps/core/imgs/default.jpg',
            'heading1': 'Heading 1',
            'heading2': 'Heading 2',
            'buttons': [
                {
                    'name': 'Button 1',
                    'link': '/#button1'
                },
                {
                    'name': 'External Button',
                    'link': 'https://www.google.com/',
                    'target': '_blank'
                }
            ]
        },
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ]
    }

    return render(request, template_name, context)


@login_required()
# @permission_required("summit_auth.view_profile.self")
def view_contact(request, profile_id=-1):
    template_name = 'registration/view_contact.html'

    try:
        profile_id = int(profile_id)
        if profile_id <= 0:
            user_profile = UserProfile.objects.get(user=request.user.id)
        else:
            user_profile = UserProfile.objects.get(id=profile_id)
        profile_details = user_profile
        projects = (Project.objects.filter(pp_i_id = profile_id) | Project.objects.filter(project_manager_id = profile_id) \
            | Project.objects.filter(staff_member_id = profile_id) | Project.objects.filter(tech_rep_id = profile_id))

        if request.user == user_profile.user:
            is_own = True
        else:
            is_own = False

        can_edit = True

        has_profile = True
    except ObjectDoesNotExist:
        has_profile = False
        is_own = False
        can_edit = False
        profile_details = ""

    context = {
        'name': 'libs.auth.view_profile',
        'pagetitle': 'Contact',
        'title': 'Your Contact',
        'bannerTemplate': 'none',
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ],
        'jsFiles': [
            'js/libs/auth/add_people_tab_bg.js'
        ],
        'profile': profile_details,
        'has_profile': has_profile,
        'is_own': is_own,
        'can_edit': can_edit,
        'projects': projects
    }

    return render(request, template_name, context)


@login_required()
@permission_required("summit_auth.edit_profile.self")
@request_test(exists_and_is_not_viewer)
def edit_contact(request, profile_id=-1):
    template_name = 'registration/edit_contact.html'

    
    try:
        profile_id = int(profile_id)
        if profile_id <= 0:
            user_profile = UserProfile.objects.get(user=request.user.id)
        else:
            user_profile = UserProfile.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        user_profile = None

    if request.method == "POST" and request.POST:
        if user_profile is None:
            user_profile = UserProfile(user=request.user)
            user_profile.save()
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        profile_form.cesu = request.session.get('cesu')
        
        print(request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.cesu.id = request.session.get('cesu')
            profile.save()
            return HttpResponseRedirect(reverse('summit.libs.auth:all_contacts')+ "?id=" +str(profile_id))
    elif user_profile is None:
        profile_form = ProfileForm()
    else:
        profile_form = ProfileForm(instance=user_profile)

    context = {
        'name': 'libs.auth.edit_profile',
        'pagetitle': 'Contact',
        'title': 'Your Contact',
        'bannerTemplate': 'none',
        'jsFiles': [
            # 'css/apps/core/testing.css'
            'js/libs/auth/add_people_tab_bg.js',
            'js/libs/auth/delete_contact.js'
        ],
        'profile': request.user.get_full_name(),
        'profile_form': profile_form,
        'contact_id': profile_id
    }

    return render(request, template_name, context)


@login_required()
#@permission_required()
def all_contacts(request, name):
    template_name = "registration/all_contacts.html"

    cesu = request.session.get('cesu')
    cesu_name = CESU.objects.get(id=cesu)
    profiles = UserProfile.objects.all().filter(cesu = cesu)
    profiles = profiles.order_by('assigned_group', 'last_name', 'first_name')
    
    if (CESURole.objects.filter(user_id=request.user.id, cesu_id=request.session.get('cesu')).exists()):
        role = CESURole.objects.get(user_id=request.user.id, cesu_id=request.session.get('cesu')).role
    elif (request.user.is_superuser):
        role = "EDITS ALLOWED" 
    else:
        role = "VIEWER" 

    print("session cesu for contacts: " + str(cesu))

    print(name)

    context = {
        'name': name,
        'pagetitle': 'All Contacts',
        'title': 'All Contacts',
        'bannerTemplate': 'none',
        'cssFiles': [
            'libs/mdb/DataTables/datatables.min.css',
            'css/datatables/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/DataTables/datatables.min.js',
            'js/datatables/no_sort_datatable.js',
            'js/libs/auth/info_display.js'
        ],
        'query': profiles,
        'cesu': cesu,
        'cesu_name': cesu_name,
        'role': role
    }

    return render(request, template_name, context)


@login_required()
#@permission_required()
def all_organizations(request, name):
    template_name = "registration/all_organizations.html"

    cesu = request.session.get('cesu')

    cesus = CESU.objects.all()
    feds = FederalAgency.objects.all()
    partner = Partner.objects.all()
    orgs = Organization.objects.all()
    if (CESURole.objects.filter(user_id=request.user.id, cesu_id=request.session.get('cesu')).exists()):
        role = CESURole.objects.get(user_id=request.user.id, cesu_id=request.session.get('cesu')).role
    elif (request.user.is_superuser):
        role = "EDITS ALLOWED" 
    else:
        role = "VIEWER" 
    

    groups = dict()

    for group in cesus:
        groups[group.id] = {
            "id": group.id,
            "name": group.name,
            "type": "CES Unit"
        }
    
    #for group in feds:
     #   groups[group.id] = {
      #      "id": group.id,
       #     "name": group.name,
        #    "type": "Federal Agency"
        #}

    #for group in partner:
    #    groups[group.id] = {
    #        "id": group.id,
    #        "name": group.name,
    #        "type": "Partner"
    #    }
    for group in orgs:
        groups[group.id] = {
            "id": group.id,
            "name": group.name,
            "type": group.type
        }

    context = {
        'name': name,
        'pagetitle': 'All Organizations',
        'title': 'All Organizations',
        'bannerTemplate': 'none',
        'cssFiles': [
            'libs/mdb/DataTables/datatables.min.css',
            'css/datatables/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/DataTables/datatables.min.js',
            'js/datatables/no_sort_datatable.js',
            'js/libs/auth/org_info.js'
        ],
        'query': groups,
        'cesu': cesu,
        'role': role
    }

    return render(request, template_name, context)

def all_users(request, name):
    template_name = "registration/all_users.html"

    cesu = request.session.get('cesu')
    cesu_name = CESU.objects.get(id=cesu)
    users = User.objects.filter(user_cesus__in=[cesu])
    users = users.order_by('last_name', 'first_name')

    context = {
        'name': name,
        'pagetitle': 'All Users',
        'title': 'All Users',
        'bannerTemplate': 'none',
        'cssFiles': [
            'libs/mdb/DataTables/datatables.min.css',
            'css/datatables/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/DataTables/datatables.min.js',
            'js/datatables/no_sort_datatable.js',
            'js/libs/auth/user_info_display.js'
        ],
        'query': users,
        'cesu': cesu,
        'cesu_name': cesu_name
    }

    return render(request, template_name, context)


@login_required()
@request_test(exists_and_is_not_viewer)
def manage_organization(request, name='summit.libs.auth.manage_organization', group_id=-1):
    template_name = "registration/manage_organization.html"

    group_id = int(group_id)
    if group_id <= 0:
        try:
            profile = UserProfile.objects.get(user=request.user)
            group_id = profile.assigned_group.id
        except (AttributeError, ObjectDoesNotExist) as e:
            return HttpResponseRedirect(reverse('summit.libs.auth:all_organizations'))

    group = get_object_or_404(UserGroup, id=group_id)

    if group is not None:
        profiles = UserProfile.objects.filter(assigned_group=group).order_by('last_name', 'first_name')
        projects = Project.objects.filter(partner_id = group_id) | Project.objects.filter(federal_agency_id = group_id)

    # Group Type
    try:
        is_cesu = CESUnit.objects.get(id=group.id)
    except ObjectDoesNotExist:
        is_cesu = False

    try:
        is_federal = FederalAgency.objects.get(id=group.id)
    except ObjectDoesNotExist:
        is_federal = False

    try:
        is_partner = Partner.objects.get(id=group.id)
    except ObjectDoesNotExist:
        is_partner = False

    try:
        is_org = Organization.objects.get(id=group.id)
    except ObjectDoesNotExist:
        is_org = False

    if is_cesu:
        group.type = "CES Unit"
    elif is_federal:
        group.type = "Federal Agency"
    elif is_partner:
        group.type = "Partner"
    else:
        group.type = "Unknown Group Type"

    context = {
        'name': name,
        'pagetitle': 'All Users in Organization',
        'title': 'All Users in Organization',
        'bannerTemplate': 'none',
        'cssFiles': [
            'libs/mdb/DataTables/datatables.min.css',
            'css/datatables/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/DataTables/datatables.min.js',
            'js/datatables/no_sort_datatable.js',
            'js/libs/auth/manage_org.js',
            'js/libs/auth/add_org_tab_bg.js',
            'js/libs/auth/filter_org_projects.js'
        ],
        'query': profiles,
        'group': group,
        'projects': projects
    }

    return render(request, template_name, context)


@login_required()
@request_test(exists_and_is_not_viewer)
def create_contact(request, name="summit.libs.auth_Create Contact", group_id=0):
    template_name = "registration/create_contact.html"

    group_id = int(group_id)

    if request.method == "POST" and request.POST:
        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile_form.cesu = request.session.get('cesu')
            print(profile_form)
            
            profile = profile_form.save(commit=False)
            profile.cesu.id = request.session.get('cesu')
            profile.save()
            return HttpResponseRedirect(reverse('summit.libs.auth:all_contacts'))
    elif group_id > 0:
        profile_form = ProfileForm(initial={'assigned_group': group_id})
    else:
        profile_form = ProfileForm()

    context = {
        'name': name,
        'pagetitle': 'Contact',
        'title': 'Create Contact',
        'bannerTemplate': 'none',
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ],
        'jsFiles': [
            'js/libs/auth/add_people_tab_bg.js'
        ],  
        'profile_form': profile_form
    }

    return render(request, template_name, context)


@login_required()
@request_test(exists_and_is_not_viewer)
def create_organization(request, name):
    template_name = "registration/create_organization.html"

    if request.method == "POST" and request.POST:
        group_form = GroupForm(request.POST, request.FILES)

        if group_form.is_valid():
            group = group_form.save()
#
#            new_org = Organization.objects.create(pk=group.id, created_on=group.created_on, name=group.name, type=group.type, description=group.description, contact=group.contact, logo=group.logo)
#            new_org.save()
            return HttpResponseRedirect(reverse('summit.libs.auth:all_organizations'))
    else:
        group_form = GroupForm()

    context = {
        'name': name,
        'pagetitle': 'Create Organization',
        'title': 'Create Organization',
        'bannerTemplate': 'none',
        'cssFiles': [
            # 'css/apps/core/testing.css'
            
        ],
        'jsFiles':
        [
            'js/libs/auth/add_tab_bg.js'
        ],
        'group_form': group_form
    }

    return render(request, template_name, context)


@login_required()
# @permission_required("summit_auth.edit_profile.self")
@request_test(exists_and_is_not_viewer)
def edit_organization(request, name="summit.libs.auth:edit_organization", group_id=-1):
    template_name = 'registration/edit_organization.html'
    is_cesu = False

    group_id = int(group_id)
    try:
        group = get_object_or_404(Organization, id=group_id)
    except:
        group = get_object_or_404(CESU, id=group_id)
        is_cesu = True

    print(group)

    if request.method == "POST" and request.POST:
        group_form = GroupForm(request.POST, request.FILES, instance=group)

        if group_form.is_valid():
            group_form_instance = group_form.instance
            print(group_form_instance)
            

            # Group Type
            print(is_cesu)
            if (is_cesu):
                group = CESU.objects.get(id=group.id)
            else:
                group = Organization.objects.get(id=group.id)
                

            if group:
                print('hey')
                #group.name=group_form_instance.name
                #group.description=group_form_instance.description
                #group.contact=group_form_instance.contact
                #if not is_cesu:
                #    group.type=group_form_instance.type
                #group.save()
                group = group_form.save()
            else:
                Organization.objects.get(id=group.id).name=group.name
                Organization.objects.get(id=group.id).name=group.description
                Organization.objects.get(id=group.id).save()

            return HttpResponseRedirect(reverse('summit.libs.auth:all_organizations'))
    else:
        group_form = GroupForm(instance=group)

    context = {
        'name': name,
        'pagetitle': 'Organization',
        'title': 'Create New Organization (Partner or CESU)',
        'bannerTemplate': 'none',
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ],
        'group_form': group_form
    }

    return render(request, template_name, context)

@login_required()
@request_test(exists_and_is_admin)
def create_user(request, name="summit.libs.auth.create_user"):
    template_name = "registration/create_user.html"

    cesu = request.session.get('cesu')
    other_users = User.objects.filter(~Q(user_cesus__in=[cesu]))

    if request.method == "POST" and request.POST:
        user_form = UserForm(request.POST, request.FILES)
        print(user_form)

        if user_form.is_valid():
            
            user_form.save()
            user_role = CESURole.objects.get_or_create(user_id=user_form.id, cesu_id=cesu)[0]
            user_role.role = request.POST['role']
            print(user_role)
            user_role.save()
            return HttpResponseRedirect(reverse('summit.libs.auth:all_users'))
    else:
        user_form = UserForm()

    context = {
        'name': name,
        'bannerTemplate': 'none',
        'cssFiles': [
            'libs/mdb/DataTables/datatables.min.css',
            'css/datatables/dashboard.css',
            # 'css/apps/core/testing.css'
        ],
        'jsFiles': [
            'js/libs/auth/add_people_tab_bg.js',
            'libs/mdb/DataTables/datatables.min.js',
            'js/datatables/dashboard.js',
            'js/libs/auth/add_existing_users.js'
        ],  
        'user_form': user_form,
        'other_users': other_users
    }

    return render(request, template_name, context)

@login_required()
@request_test(exists_and_is_admin)
def edit_user(request, profile_id=-1, name="libs.auth.edit_user"):
    template_name = 'registration/edit_user.html'

    try:
        cesu = request.session.get('cesu')
        profile_id = int(profile_id)
        if profile_id <= 0:
            user_profile = User.objects.get(user=request.user.id)
            #role_id = CESURole.objects.get(user_id=request.user.id, cesu_id=cesu)
        else:
            user_profile = User.objects.get(id=profile_id)
            #role_id = CESURole.objects.get(user_id=profile_id, cesu_id=cesu)
    except ObjectDoesNotExist:
        user_profile = None

    if request.method == "POST" and request.POST:
        if user_profile is None:
            user_profile = User(user=request.user)
            user_profile.save()
        profile_form = UserForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():
            print(request.POST)
            profile = profile_form.save()
            user_role = CESURole.objects.get_or_create(user_id=profile_id, cesu_id=cesu)[0]
            user_role.role = request.POST['role']
            print(user_role)
            user_role.save()
            return HttpResponseRedirect(reverse('summit.libs.auth:all_users'))
    elif user_profile is None:
        profile_form = UserForm()
        role_form = RoleForm()
    else:
        profile_form = UserForm(instance=user_profile)
        role_form = RoleForm()

    context = {
        'name': 'libs.auth.edit_user',
        'pagetitle': 'Edit User',
        'title': 'Edit User',
        'bannerTemplate': 'none',
        'jsFiles': [
            # 'css/apps/core/testing.css'
            'js/libs/auth/add_people_tab_bg.js'
        ],
        'profile': request.user.get_full_name(),
        'user_form': profile_form,
    }

    return render(request, template_name, context)

def info_display(request):
    if request.is_ajax():
        print(request.GET)
        userID = request.GET.get('userID')
        cesuID = request.GET.get('cesuID')
        userInfo = UserProfile.objects.filter(cesu = cesuID)
        userInfo = userInfo.filter(id = userID).values()
        ProjectInfo = Project.objects.filter(cesu_unit = cesuID)
        ProjectInfo = ProjectInfo.filter(pp_i_id = userID) | ProjectInfo.filter(project_manager_id = userID) | ProjectInfo.filter(tech_rep_id = userID) | ProjectInfo.filter(staff_member_id = userID)
        ProjectInfo = ProjectInfo.values()
        return JsonResponse({"user": list(userInfo) , "projects": list(ProjectInfo)})

    userInfo = UserProfile.objects.get(id = 0).values()
    groupInfo = UserGroup.objects.filter(id = 0).values()
    return JsonResponse({"user": list(userInfo)})

def user_info_display(request):
    if request.is_ajax():
        print(request.GET)
        userID = request.GET.get('userID')
        requested_user = User.objects.filter(id = userID)
        userInfo = requested_user.values()
        associated_cesus = requested_user[0].user_cesus.all().values()
        return JsonResponse({"user": list(userInfo), "cesus": list(associated_cesus)})

    userInfo = User.objects.get(id = 0).values()
    return JsonResponse({"user": list(userInfo)})

def delete_contact(request):
    if request.is_ajax():
        print("deleting contact...")
       
        userID = request.POST.get('contactID')
        user = UserProfile.objects.get(id = userID)
        print(user.first_name)
        user.delete()
        print(user.first_name)
        return_user = UserProfile.objects.filter(id = userID).values()
        return JsonResponse({"contact": list(return_user)})
    print("contact not deleted!")
    return_user = UserProfile.objects.filter(id = userID).values()
    return JsonResponse({"contact": list(return_user)})

def org_info(request):
    if request.is_ajax():
        print(request.GET)
        groupID = request.GET.get('groupID')
        cesuID = request.GET.get('cesuID')
        org = Organization.objects.filter(id = groupID).values()
        people = UserProfile.objects.filter(cesu = cesuID)
        people = people.filter(assigned_group_id = groupID).values()
        projects = Project.objects.filter(cesu_unit_id = cesuID)
        projects = projects.filter(partner_id = groupID).values() | projects.filter(federal_agency_id = groupID).values()
        return JsonResponse({"people": list(people), "projects": list(projects), "org": list(org)})
    people = UserProfile.objects.all().values()
    projects = Project.objects.all().values()
    return JsonResponse({"people": list(people), "projects": list(projects)})

def deactivate_user(request):
    if request.is_ajax():
        userID = request.POST.get('userID')
        reactivate = request.POST.get('reactivate')
        print(reactivate)
        user = User.objects.get(id = userID)
        if (reactivate == "true"):
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return_user = User.objects.filter(id = userID).values()
        return JsonResponse({"user": list(return_user)})
    return_user = User.objects.filter(id = userID).values()
    return JsonResponse({"user": list(return_user)})

def delete_user(request):
    if request.is_ajax():
        userID = request.POST.get('userID')
        user = User.objects.get(id = userID)
        user.delete()
        return_user = User.objects.filter(id = userID).values()
        return JsonResponse({"user": list(return_user)})
    return_user = User.objects.filter(id = userID).values()
    return JsonResponse({"user": list(return_user)})



@request_test(exists_and_is_admin)
def add_users(request):
    if request.is_ajax():
        
        userIDs = request.POST.getlist('userIDs[]')
        print(userIDs)
        cesuID = request.session.get('cesu')
        for userID in userIDs:
            print(userID)
            user = User.objects.get(id = userID)
            user.user_cesus.add(CESU.objects.get(id=cesuID))
        return JsonResponse({"userIDS": list(userIDs)})
    userIDs = request.POST.getlist('userIDs')
    return JsonResponse({"userIDS": list(userIDs)})