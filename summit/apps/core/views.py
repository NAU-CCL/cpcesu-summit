from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from django.core.exceptions import ObjectDoesNotExist
from summit.libs.auth.models import UserProfile, CESU
from summit.apps.projects.models import Project

def index(request):
    template_name = 'apps/core/index.html'

    context = {
        'pagetitle': 'Home',
        'title': 'Home page',
        'bannerTemplate': 'fullscreen',
        'header': {
            'heading1': 'Welcome to Summit',
            'heading2': 'Your New Cooperative Ecosystem Studies Unit Project Management System',
            'buttons': [
                {
                    'name': ('Your Dashboard' if request.user.is_authenticated
                             else 'Current Projects'),
                    'link': ("summit.libs.auth:cesu_selector" if request.user.is_authenticated
                             else "summit.apps.projects:project_public_list"),
                    'uses_reverse': True
                }
                
            ]
        },
        'cssFiles': [
        ]
    }

    return render(request, template_name, context)

class MainView(ListView):
    template_name = 'apps/core/index.html'
    model = Project
    context_object_name = 'projects'

    permission_required = 'summit_projects.add_project'
    permission_denied_message = 'You do not have the correction permissions to access this page.'
    #raise_exception = False



    def get_context_data(self, **kwargs):
        if (self.request.user):
            user = self.request.user
        cesu = self.request.session.get('cesu')
        print(self.request.session.get('cesu_image'))

        print("session cesu: " + str(cesu))
        print(user)
        cesu_list = CESU.objects.all()

        profile = None

        if (user.id):
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
            'header': {
                'heading1': 'Welcome to Summit',
                'heading2': 'Your New Cooperative Ecosystem Studies Unit Project Management System',
                'buttons': [
                    {
                        'name': ('Your Dashboard' if self.request.user.is_authenticated
                                else 'Current Projects'),
                        'link': ("summit.libs.auth:cesu_selector" if self.request.user.is_authenticated
                                else "summit.apps.projects:project_public_list"),
                        'uses_reverse': True
                    }
                    
                ]
            },
            'bannerTemplate': 'fullscreen',
            "cesu_list": cesu_list

        }
        ctx = super(MainView, self).get_context_data(**kwargs)
        ctx = {**ctx, **context}
        return ctx

def about(request, name):
    template_name = 'apps/core/about.html'

    context = {
        'name': name,
        'pagetitle': 'About',
        'title': 'About the CPCESU',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
    }

    return render(request, template_name, context)
