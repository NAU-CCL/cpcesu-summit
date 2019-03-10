from summit.apps.projects.models import Notification


def notification_context_processor(request):
    return {
        'notifications': Notification.objects.all(),
    }
