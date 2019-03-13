# TODO: Determine if each project title is unique (Ask CP)
from django.db import models
from config.links import get_name
from django.core.validators import MinValueValidator
from django.core.files.storage import FileSystemStorage
from django.conf import settings
#import datetime
from django.utils import timezone
import pytz
from decimal import Decimal
from django.contrib.auth.models import User

from summit.libs.auth.models import Partner, FederalAgency, CESUnit

# TODO: Create help text for each field.
_help_text = {
    'project_title': 'The title of the project',
    'short_summary': 'This field is displayed in "overviews" such as the projects listing page.',
    'description': 'A free-form description of the plugin.',
    'sensitive': 'True if data is sensitive and cannot be revealed to the public.',
    'budget': 'Any amount that pertains to the overall budget of a project.',
    'student_support': 'A project may have support from students.',
}


class Project(models.Model):

    def project_directory_path(self, filename):
        return 'projects/{0}/{1}'.format(self.project_title, filename)

    GRADUATE = 'GRAD'
    UNDERGRADUATE = 'UGRAD'
    BOTH = 'BOTH'
    NONE = 'NONE'
    DRAFTING = 'DRAFT'
    EXECUTED = 'EXEC'
    CLOSED = 'CLOSE'
    STUDENT_SUPPORT = (
        (GRADUATE, 'Graduate'),
        (UNDERGRADUATE, 'Undergraduate'),
        (BOTH, 'Graduate and Undergraduate'),
        (NONE, 'None')
    )
    STATUS = (
        (DRAFTING, 'Drafting'),
        (EXECUTED, 'Executed'),
        (CLOSED, 'Closed')
    )

    project_title = models.CharField(max_length=500, unique=True, help_text=_help_text['project_title'])
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'])
    description = models.TextField(help_text=_help_text['description'])
    sensitive = models.BooleanField(default=False, help_text=_help_text['sensitive'])
    budget = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['budget'])
    student_support = models.CharField(max_length=5, choices=STUDENT_SUPPORT, default=NONE)
    status = models.CharField(max_length=5, choices=STATUS, default=DRAFTING)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE,
                                related_name='partner', default=None, blank=True, null=True)
    federal_agency = models.ForeignKey(FederalAgency, on_delete=models.CASCADE,
                                       related_name='federal_agency', default=None, blank=True, null=True)
    cesu_unit = models.ForeignKey(CESUnit, on_delete=models.CASCADE,
                                  related_name='cesu_unit', default=None, blank=True, null=True)
    # TODO: Read file in 'chunks' ---> https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
    # TODO: Create File model
    file = models.FileField(upload_to=project_directory_path,
                            default=str(settings.MEDIA_ROOT) + '/projects/default.txt')

    date = models.DateTimeField(default=timezone.now, blank=True)
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('summit.apps.projects:project-detail', args=[str(self.id)])

    def __str__(self):
        return self.project_title


class Notification(models.Model):
    TYPE_OPTIONS = (
        ('CHECKUP', 'Checkup'),
        ('NONE', 'None'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default='NONE')
    description = models.TextField(help_text=_help_text['description'])
    seen = models.BooleanField(default=False)

    #def mark_seen(self):
    #    self.seen = True

    def __str__(self):
        return self.description


class ProjectFiles(models.Model):
    def project_directory_path(self, filename):
        return 'projects/{0}'.format(filename)

    file = models.FileField(upload_to=project_directory_path,
                            default=str(settings.MEDIA_ROOT))

    def get_absolute_url(self):
        return u'create'
