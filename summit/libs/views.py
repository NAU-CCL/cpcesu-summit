from django.shortcuts import render


def error404(request):
    template_name = 'libs/error.html'

    context = {
        'name': 'Error',
        'pagetitle': 'Error',
        'title': 'That\'s an Error',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
        'error_msg': 'Error 404 - Page Not Found',
        'error_desc': 'Please check the URL and try again. If you feel like this is an error, please submit feedback \
            below.'
    }

    return render(request, template_name, context=context, status=404)
