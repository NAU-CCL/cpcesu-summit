from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render


from .forms import ProfileForm, GroupForm
from .models import User, UserProfile, UserGroup, CESUnit, FederalAgency, Partner, CESU, Organization
from summit.apps.projects.models import Project


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

        if profile_form.is_valid():
            profile = profile_form.save()
            if profile.user is not None and profile.user.id == request.user.id:
                return HttpResponseRedirect(reverse('summit.libs.auth:all_contacts'))
            else:
                return HttpResponseRedirect(reverse('summit.libs.auth:all_contacts'))
    elif user_profile is None:
        profile_form = ProfileForm()
    else:
        profile_form = ProfileForm(instance=user_profile)

    context = {
        'name': 'libs.auth.edit_profile',
        'pagetitle': 'Contact',
        'title': 'Your Contact',
        'bannerTemplate': 'none',
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ],
        'profile': request.user.get_full_name(),
        'profile_form': profile_form
    }

    return render(request, template_name, context)


@login_required()
#@permission_required()
def all_contacts(request, name):
    template_name = "registration/all_contacts.html"

    profiles = UserProfile.objects.all().order_by('assigned_group', 'last_name', 'first_name')

    print(name)

    context = {
        'name': name,
        'pagetitle': 'All Contacts',
        'title': 'All Contacts',
        'bannerTemplate': 'none',
        'cssFiles': [
            'libs/mdb/css/addons/datatables.min.css',
            'css/datatables/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/js/addons/datatables.min.js',
            'js/datatables/no_sort_datatable.js',
            'js/libs/auth/info_display.js'
        ],
        'query': profiles
    }

    return render(request, template_name, context)


@login_required()
#@permission_required()
def all_organizations(request, name):
    template_name = "registration/all_organizations.html"

    cesus = CESU.objects.all()
    feds = FederalAgency.objects.all()
    partner = Partner.objects.all()
    orgs = Organization.objects.all()

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
            'libs/mdb/css/addons/datatables.min.css',
            'css/datatables/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/js/addons/datatables.min.js',
            'js/datatables/no_sort_datatable.js',
            'js/libs/auth/org_info.js'
        ],
        'query': groups
    }

    return render(request, template_name, context)


@login_required()
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
            'libs/mdb/css/addons/datatables.min.css',
            'css/datatables/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/js/addons/datatables.min.js',
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
def create_contact(request, name="summit.libs.auth_Create Contact", group_id=0):
    template_name = "registration/create_contact.html"

    group_id = int(group_id)

    if request.method == "POST" and request.POST:
        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile_form.save()
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
        'profile_form': profile_form
    }

    return render(request, template_name, context)


@login_required()
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
        'group_form': group_form
    }

    return render(request, template_name, context)


@login_required()
# @permission_required("summit_auth.edit_profile.self")
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
                group.name=group_form_instance.name
                group.description=group_form_instance.description
                group.contact=group_form_instance.contact
                if not is_cesu:
                    group.type=group_form_instance.type
                group.save()
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

def info_display(request):
    if request.is_ajax():
        print(request.GET)
        userID = request.GET.get('userID')
        userInfo = UserProfile.objects.filter(id = userID).values()
        ProjectInfo = Project.objects.filter(pp_i_id = userID) | Project.objects.filter(project_manager_id = userID)
        ProjectInfo = ProjectInfo.values()
        return JsonResponse({"user": list(userInfo) , "projects": list(ProjectInfo)})

    userInfo = UserProfile.objects.get(id = 0).values()
    groupInfo = UserGroup.objects.filter(id = 0).values()
    return JsonResponse({"user": list(userInfo)})

def org_info(request):
    if request.is_ajax():
        print(request.GET)
        groupID = request.GET.get('groupID')
        people = UserProfile.objects.filter(assigned_group_id = groupID).values()
        projects = Project.objects.filter(partner_id = groupID).values() | Project.objects.filter(federal_agency_id = groupID).values()
        return JsonResponse({"people": list(people), "projects": list(projects)})
    people = UserProfile.objects.all().values()
    projects = Project.objects.all().values()
    return JsonResponse({"people": list(people), "projects": list(projects)})