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
            'customClasses': 'button'
        },
    ],
    [
        {
            'pageId': 'apps.core.send_feedback',
            'name': 'Send Feedback',
            'link': '/'
        },
        {
            'pageId': 'apps.docs.index',
            'name': 'Documentation',
            'link': '/'
        },
    ]
]


def get():
    return links
