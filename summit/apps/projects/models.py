# TODO: Add project fields based on requirements
# TODO: Determine if each project title is unique (Ask CP)
# TODO: Update student support
from django.db import models


_help_text = {
    'project_title': 'The title of the project',
    'short_summary': 'This field is displayed in "overviews" such as the projects listing page.',
    'description': 'A free-form description of the plugin.',
    'sensitive': 'True if data is sensitive and cannot be revealed to the public.',
    'budget': 'Any amount that pertains to the overall budget of a project.',
    'student_support': 'A project may have support from students.',
}


class Project(models.Model):
    GRADUATE = 'GRAD'
    PRE_GRAD = 'PREGRAD'
    NA = 'NONE'
    STUDENT_SUPPORT = (
        (GRADUATE, 'Graduate'),
        (PRE_GRAD, 'Pre-Graduate'),
        (NA, 'None')
    )

    project_title = models.CharField(max_length=500, unique=True, help_text=_help_text['project_title'])
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'])
    description = models.TextField(help_text=_help_text['description'])
    sensitive = models.BooleanField(default=False, help_text=_help_text['sensitive'])
    budget = models.CharField(max_length=100, help_text=_help_text['budget'])
    student_support = models.CharField(max_length=1, choices=STUDENT_SUPPORT, default=NA)
