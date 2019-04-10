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
        'pageId': 'libs.auth.logged_out',
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
@permission_required("summit_auth.view_profile.self")
def view_profile(request, profile_id=-1):
    template_name = 'registration/view_profile.html'

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
        profile_details = ""

    context = {
        'pageId': 'libs.auth.view_profile',
        'pagetitle': 'Profile',
        'title': 'Your Profile',
        'header': {
            'background': 'apps/core/imgs/default.jpg'
        },
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
def edit_profile(request, profile_id=-1):
    template_name = 'registration/edit_profile.html'

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
        'pageId': 'libs.auth.edit_profile',
        'pagetitle': 'Profile',
        'title': 'Your Profile',
        'header': {
            'background': 'apps/core/imgs/default.jpg'
        },
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ],
        'profile': request.user.get_full_name(),
        'profile_form': profile_form
    }

    return render(request, template_name, context)


@login_required()
#@permission_required()
def all_users(request, name):
    template_name = "auth/all_users.html"

    profiles = UserProfile.objects.all()

    context = {
        'pageId': name,
        'pagetitle': 'All Groups and Users',
        'title': 'All Groups and Users',
        'cssFiles': [
            'libs/mdb/css/addons/datatables.min.css',
            'css/apps/projects/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/js/addons/datatables.min.js',
            'js/apps/projects/dashboard.js'
        ],
        'query': profiles
    }

    return render(request, template_name, context)


@login_required()
def manage_group(request, name='summit.libs.auth.manage_group', group_id=-1):
    template_name = "auth/manage_group.html"

    group_id = int(group_id)
    if group_id <= 0:
        group_id = request.user.group.id

    group = get_object_or_404(UserGroup, id=group_id)

    if group is not None:
        profiles = UserProfile.objects.filter(assigned_group=group)

    context = {
        'pageId': name,
        'pagetitle': 'All Groups and Users',
        'title': 'All Groups and Users',
        'cssFiles': [
            'libs/mdb/css/addons/datatables.min.css',
            'css/apps/projects/dashboard.css'
        ],
        'jsFiles': [
            'libs/mdb/js/addons/datatables.min.js',
            'js/apps/projects/dashboard.js'
        ],
        'query': profiles,
        'group': group
    }

    return render(request, template_name, context)


@login_required()
def create_profile(request, name="summit.libs.auth_Create User", group_id=0):
    template_name = "auth/create_user.html"

    group_id = int(group_id)

    if request.method == "POST" and request.POST:
        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('summit.libs.auth2:summit.libs.auth2_All Groups and Users'))
    elif group_id > 0:
        profile_form = ProfileForm(initial={'assigned_group': group_id})
    else:
        profile_form = ProfileForm()

    context = {
        'pageId': name,
        'pagetitle': 'Profile',
        'title': 'Create User Profile',
        'header': {
            'background': 'apps/core/imgs/default.jpg'
        },
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ],
        'profile_form': profile_form
    }

    return render(request, template_name, context)


@login_required()
def create_group(request, name):
    template_name = "auth/create_group.html"

    if request.method == "POST" and request.POST:
        group_form = GroupForm(request.POST, request.FILES)

        if group_form.is_valid():
            group = group_form.save()

            if group_form.cleaned_data['group_type'] == 1:
                cesu = CESUnit(group)
                cesu.save()
            elif group_form.cleaned_data['group_type'] == 2:
                federal = FederalAgency(group)
                federal.save()
            elif group_form.cleaned_data['group_type'] == 3:
                partner = Partner(group)
                partner.save()

            return HttpResponseRedirect(reverse('summit.libs.auth2:summit.libs.auth2_All Groups and Users'))
    else:
        group_form = GroupForm()

    context = {
        'pageId': name,
        'pagetitle': 'User Group',
        'title': 'Create User Group',
        'header': {
            'background': 'apps/core/imgs/default.jpg'
        },
        'cssFiles': [
            # 'css/apps/core/testing.css'
        ],
        'group_form': group_form
    }

    return render(request, template_name, context)
