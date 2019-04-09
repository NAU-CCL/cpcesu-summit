from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery, current_task
from celery.schedules import crontab
from .models import Notification, Project, Partner, CESUnit, FederalAgency
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField
from .ocr import collect_data
from celery.utils.log import get_task_logger


app = Celery('mysite',
             broker='redis://',
             backend='redis://',
             include=['apps.polls.tasks'])

logger = get_task_logger(__name__)


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


@app.task(bind=True)
def read_pdf(self, filename):
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 33})
    print('\n\n\n\nHEREHRHERHERHERHREHERRHEH\n')
    logger.info('HEREHREHRE request id: {0}'.format(self.request.id))
    print(self.request.id)
    data = collect_data(filename)
    print('\n\n\n\nHEREHRHERHERHERHREHERRHEH\n')
    logger.info('HEREHREHRE request id: {0}'.format(self.request.id))
    print(self.request.id)
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 66})
    print('\n\n\n\nHEREHRHERHERHERHREHERRHEH\n')
    logger.info('HEREHREHRE request id: {0}'.format(self.request.id))
    print(self.request.id)

    new_project = Project.objects.create(cesu_unit_id=33,
                                         project_title=data.get('project_title'),
                                         short_summary=data.get('purpose'),
                                         description='this',
                                         budget=100,
                                         job_id=str(self.request.id),)
    print('\n\n\n\nHEREHRHERHERHERHREHERRHEH\n')
    logger.info('HEREHREHRE request id: {0}'.format(self.request.id))
    print(self.request.id)

    new_project.save()
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 100})
