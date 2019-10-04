from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery, current_task
from celery.schedules import crontab
from .models import Project, Partner, CESUnit, FederalAgency
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField
from .ocr import collect_data
from celery.utils.log import get_task_logger
from . import choices


app = Celery('mysite',
             broker='redis://',
             backend='redis://',
             include=['apps.polls.tasks'])

logger = get_task_logger(__name__)


@app.task
def test(arg):
    print(arg)


# @app.task
# def test_notification():
#     """ need to check if project and issue already exists in the database """
#     min_days_to_notify = 30
#     threshold = timezone.now() - timedelta(days=min_days_to_notify)
#     all_projects = Project.objects.filter(date__lt=threshold)
#
#     for project in all_projects:
#         cur_notifications = Notification.objects.filter(project=project, type='CHECKUP')
#         if cur_notifications.count() == 0:
#             new_notification = Notification(project=project,
#                                             type='CHECKUP',
#                                             description='Project hasnt been updated for 30 days')
#             new_notification.save()


@app.task(bind=True)
def read_pdf(self, filename):
    print("Working...")
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 0})

    print("Collecting data...")
    data = collect_data(filename)

    print("Updating progress...")
    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 90})

    # May need to create cesu object or search somehow
    budget = data['aw_total'].replace('$', '')
    budget = budget.replace(',', '')
    budget = budget.split('.')[0]
    budget = int(budget)
    tent_start_date = datetime.strptime(data['effective_date'], '%m/%d/%Y')
    tent_end_date = datetime.strptime(data['completion_date'], '%m/%d/%Y')

    current_task.update_state(state='PROGRESS',
                              meta={'process_percent': 95})

    STATUS = choices.ProjectChoices.STATUS
    print("STATUS: ", STATUS)

    logger.info('Request id: {0}'.format(self.request.id))
    print(self.request.id)

    new_project = Project(
        budget=budget,
        # cesu_unit_id=,
        # description=,
        # discipline='',
        # exec_start_date=,
        # federal_agency=NULL,
        # field_of_science=,
        # final_report=,
        # fiscal_year=,
        # location=,
        # init_start_date=,
        # monitoring=,
        notes=data['purpose'],
        # num_of_students=,
        p_num=data['agreement_number'],
        # partner=,
        # pp_i=,
        # project_manager=,
        project_title=data['project_title'],
        # r_d=,
        # reviewed=,
        # sci_method=,
        # sensitive=,
        # short_summary=,
        # src_of_funding=,
        # staff_member=,
        status=STATUS[1],
        # tech_rep=,
        tent_end_date=tent_end_date,
        tent_start_date=tent_start_date,
        # type=,
        # vet_support=,
        # short_summary=data.get('purpose'),
        job_id=str(self.request.id),
    )

    print("SAVING PROJECT")
    proj = new_project.save(force_insert=True)

    print("Check proj - ", proj)
    proj2 = new_project.save()
    print("Check proj2 - ", proj2)
    current_task.update_state(state='COMPLETE',
                              meta={'process_percent': 100})
