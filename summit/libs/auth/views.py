from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


from .forms import ProfileForm
from .models import UserProfile


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
def view_profile(request):
    template_name = 'registration/view_profile.html'

    try:
        user_profile = UserProfile.objects.get(user=request.user.id)
        profile_details = user_profile
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
        'has_profile': has_profile
    }

    return render(request, template_name, context)


@login_required()
@permission_required("summit_auth.edit_profile.self")
def edit_profile(request):
    template_name = 'registration/edit_profile.html'

    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST" and request.POST:
        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():
            profile_form.save()

        return HttpResponseRedirect('profile')
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
