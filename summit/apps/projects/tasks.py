from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery, current_task
from celery.schedules import crontab
from .models import Notification, Project, Partner, CESUnit, FederalAgency
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField
from .ocr import collect_data


app = Celery('mysite',
             broker='redis://',
             backend='redis://',
             include=['apps.polls.tasks'])


@app.task
def test(arg):
    print(arg)


@app.task
def test_notification():
    """ need to check if project and issue already exists in the database """
    min_days_to_notify = 30
    threshold = timezone.now() - timedelta(days=min_days_to_notify)
    all_projects = Project.objects.filter(date__lt=threshold)

    for project in all_projects:
        cur_notifications = Notification.objects.filter(project=project, type='CHECKUP')
        if cur_notifications.count() == 0:
            new_notification = Notification(project=project,
                                            type='CHECKUP',
                                            description='Project hasnt been updated for 30 days')
            new_notification.save()


@shared_task
def read_pdf(filename):
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 33})
    data = collect_data(filename)
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 66})
    new_project = Project.objects.create(cesu_unit_id=33,
                                         project_title=data.get('project_title'),
                                         short_summary=data.get('purpose'),
                                         description='this',
                                         budget=100,)

    new_project.save()
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 100})
