from django.shortcuts import render


def error400(request):
    template_name = 'libs/error.html'

    context = {
        'name': 'Error',
        'pagetitle': 'Error',
        'title': 'That\'s an Error',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
        'error_msg': 'Error 400 - Bad Request',
        'error_desc': 'Please go back and try your request again. If you feel like this is an error, please submit \
            feedback below.'
    }

    return render(request, template_name, context=context, status=400)


def error403(request):
    template_name = 'libs/error.html'

    context = {
        'name': 'Error',
        'pagetitle': 'Error',
        'title': 'That\'s an Error',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
        'error_msg': 'Error 403 - Forbidden',
        'error_desc': 'Please check if you are logged in. If you are, check the URL and see if you have access. If \
            you feel like this is an error, please submit feedback below.'
    }

    return render(request, template_name, context=context, status=403)


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


def error500(request):
    template_name = 'libs/error.html'

    context = {
        'name': 'Error',
        'pagetitle': 'Error',
        'title': 'That\'s an Error',
        'header': {
            'background': 'imgs/coverImages/canyon-country-2400x600.jpg',
        },
        'error_msg': 'Error 500 - Server Error',
        'error_desc': 'Please go back and try your request again. If you feel like this is an error, please submit \
            feedback below.'
    }

    return render(request, template_name, context=context, status=500)
