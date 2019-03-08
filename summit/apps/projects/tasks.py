from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery
from celery.schedules import crontab
from .models import Notification, Project
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField


app = Celery('mysite',
             broker='redis://',
             backend='redis://',
             include=['apps.polls.tasks'])




@app.task
def add(x, y):
    return x + y


@app.task
def test(arg):
    print(arg)


@app.task
def test_notification():
    '''need to check if project and issue already exists in the database'''
    min_days_to_notify = 30
    threshold = timezone.now() - timedelta(days=min_days_to_notify)
    all_projects = Project.objects.filter(date__lt=threshold)

    for project in all_projects:
        cur_notifications = Notification.objects.filter(project=project, type='CHECKUP')
        print("HERHEHREHERE" + str(cur_notifications))
        if cur_notifications.count() == 0:
            new_notification = Notification(project=project,
                                            type='CHECKUP',
                                            description='Project hasnt been updated for 30 days')
            new_notification.save()
