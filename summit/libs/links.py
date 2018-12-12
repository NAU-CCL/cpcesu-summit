from django.conf import settings

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
    ],
    [
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
