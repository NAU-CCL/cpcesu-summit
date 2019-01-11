from django.urls import reverse

links = [
    [
        {
            'pageId': 'apps.core.home',
            'name': 'Home',
            'link': '/'
        },
        {
            'pageId': 'apps.core.about',
            'name': 'About',
            'link': '/about/'
        },
        {
            'pageId': 'contact.index',
            'name': 'Contact',
            'link': '/',
        },
        {
            'pageId': 'apps.projects.index',
            'name': 'Projects',
            'link': reverse('summit.apps.projects:project-list'),
            'login_required': True
        }
    ],
    [
        {
            'pageId': '',
            'name': 'Admin Site',
            'link': reverse("admin:index"),
            'customClasses': 'btn btn-red btn-sm',
            'login_required': True,
            'staff_only': True
        },
        {
            'pageId': 'apps.core.send_feedback',
            'name': 'Send Feedback',
            'link': '/',
            'customClasses': 'btn btn-primary btn-sm'
        },
        {
            'pageId': 'apps.docs.index',
            'name': 'Documentation',
            'link': '/docs',
            'customClasses': 'btn btn-primary btn-sm'
        },
    ]
]


def get():
    return links
