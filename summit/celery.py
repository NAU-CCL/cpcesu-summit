from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
#from summit.apps.projects.tasks import test_notification
#import .celeryconfig #import Celeryconfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.shared')

# app = Celery('summit')
app = Celery('mysite',
             broker='redis://',
             backend='redis://',)
             #include=['apps.projects.tasks'],)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notify_30_day_old_projects': {
        'task': 'summit.apps.projects.tasks.test_notification',
        'schedule': crontab(hour=2, minute=28, day_of_week=3), #15,  #
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
