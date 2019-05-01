from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


from .forms import ProfileForm, GroupForm
from .models import User, UserProfile, UserGroup, CESUnit, FederalAgency, Partner


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
        'profile': profile_details,
        'has_profile': has_profile,
        'is_own': is_own,
        'can_edit': can_edit
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
                return HttpResponseRedirect(reverse('summit.libs.auth:view_profile'))
            else:
                return HttpResponseRedirect(reverse('summit.libs.auth:view_profile_other', kwargs={'profile_id': profile.id}))
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
            'js/datatables/no_sort_datatable.js'
        ],
        'query': profiles
    }

    return render(request, template_name, context)


@login_required()
#@permission_required()
def all_organizations(request, name):
    template_name = "registration/all_organizations.html"

    cesus = CESUnit.objects.all()
    feds = FederalAgency.objects.all()
    partner = Partner.objects.all()

    groups = dict()

    for group in cesus:
        groups[group.id] = {
            "id": group.id,
            "name": group.name,
            "type": "CES Unit"
        }

    for group in feds:
        groups[group.id] = {
            "id": group.id,
            "name": group.name,
            "type": "Federal Agency"
        }

    for group in partner:
        groups[group.id] = {
            "id": group.id,
            "name": group.name,
            "type": "Partner"
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
            'js/libs/auth/group_sort.js'
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
            return HttpResponseRedirect(reverse('summit.libs.auth2:summit.libs.auth2_All Groups'))

    group = get_object_or_404(UserGroup, id=group_id)

    if group is not None:
        profiles = UserProfile.objects.filter(assigned_group=group).order_by('last_name', 'first_name')

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
            'js/datatables/no_sort_datatable.js'
        ],
        'query': profiles,
        'group': group
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
            return HttpResponseRedirect(reverse('summit.libs.auth2:summit.libs.auth2_All Contacts'))
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

            group_type = group_form['group_type'].value()

            group_type = int(group_type)

            if group_type == 1:
                cesu = CESUnit.objects.create(pk=group.id, created_on=group.created_on, name=group.name, description=group.description, avatar=group.avatar)
                cesu.save()
            elif group_type == 2:
                federal = FederalAgency.objects.create(pk=group.id, created_on=group.created_on, name=group.name, description=group.description, avatar=group.avatar)
                federal.save()
            elif group_type == 3:
                partner = Partner.objects.create(pk=group.id, created_on=group.created_on, name=group.name, description=group.description, avatar=group.avatar)
                partner.save()

            return HttpResponseRedirect(reverse('summit.libs.auth2:summit.libs.auth2_All Orgs.'))
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
def edit_organization(request, name="summit.libs.auth2:summit.libs.auth2_edit_organization", group_id=-1):
    template_name = 'registration/edit_organization.html'

    group_id = int(group_id)
    group = get_object_or_404(UserGroup, id=group_id)

    if request.method == "POST" and request.POST:

        group_form = GroupForm(request.POST, request.FILES, instance=group)

        if group_form.is_valid():
            group = group_form.instance

            new_group_type = group_form['group_type'].value()

            new_group_type = int(new_group_type)

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

            if is_cesu:
                is_cesu.delete()
            elif is_federal:
                is_federal.delete()
            elif is_partner:
                is_partner.delete()
            else:
                UserGroup.objects.get(id=group.id).delete()

            if new_group_type == 1:
                cesu = CESUnit.objects.create(pk=group.id, created_on=group.created_on, name=group.name,
                                              description=group.description, avatar=group.avatar)
                cesu.save()
            elif new_group_type == 2:
                federal = FederalAgency.objects.create(pk=group.id, created_on=group.created_on, name=group.name,
                                                       description=group.description, avatar=group.avatar)
                federal.save()
            elif new_group_type == 3:
                partner = Partner.objects.create(pk=group.id, created_on=group.created_on, name=group.name,
                                                 description=group.description, avatar=group.avatar)
                partner.save()

            return HttpResponseRedirect(reverse('summit.libs.auth2:manage_group_other', kwargs={'group_id': group_id}))
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
