# TODO: Add project fields based on requirements
# TODO: Determine if each project title is unique (Ask CP)
# TODO: Update student support
from django.db import models

from django.core.validators import MinValueValidator

from decimal import Decimal


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
    UNDERGRADUATE = 'UGRAD'
    BOTH = 'BOTH'
    NONE = 'NONE'
    STUDENT_SUPPORT = (
        (GRADUATE, 'Graduate'),
        (UNDERGRADUATE, 'Undergraduate'),
        (BOTH, 'Graduate and Undergraduate'),
        (NONE, 'None')
    )

    project_title = models.CharField(max_length=500, unique=True, help_text=_help_text['project_title'])
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'])
    description = models.TextField(help_text=_help_text['description'])
    sensitive = models.BooleanField(default=False, help_text=_help_text['sensitive'])
    budget = models.DecimalField(validators=[MinValueValidator(0.001)], max_digits=12, decimal_places=3, help_text=_help_text['budget'])
    student_support = models.CharField(max_length=5, choices=STUDENT_SUPPORT, default=NONE)

    def __str__(self):
        return self.project_title
