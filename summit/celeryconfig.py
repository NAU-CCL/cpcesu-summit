from celery import shared_task, Celery
from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis'

#task_serializer = 'json'
#result_serializer = 'json'
#accept_content = ['json']
#timezone = 'Europe/Oslo'
enable_utc = True

app = Celery('mysite',
             broker='redis://',
             backend='redis://',)
             #include=['apps.projects.tasks'],)

# 30.0 for seconds

app.conf.beat_schedule = {
    'notify_30_day_old_projects': {
        'task': 'tasks.test_notification',
        'schedule': crontab(hour=2, minute=28, day_of_week=3), #60,#
    },
}

