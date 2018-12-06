from django.conf import settings

links = [
    {
        'pageId': 'core.home',
        'name': 'Home',
        'link': '/'
    },
    {
        'pageId': 'core.about',
        'name': 'About',
        'link': '/about/'
    },
    {
        'pageId': 'polls.index',
        'name': 'Polls',
        'link': '/polls/'
    },
    {
        'pageId': 'contact.index',
        'name': 'Contact',
        'link': '/',
        'customClasses': 'button'
    }
]

def get():
    return links
