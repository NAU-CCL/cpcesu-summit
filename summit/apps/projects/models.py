# TODO: Determine if each project title is unique (Ask CP)
from django.db import models
from config.links import get_name
from django.core.validators import MinValueValidator
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import datetime
from decimal import Decimal

from summit.libs.auth.models import Partner, FederalAgency, CESUnit

# TODO: Create/Update help text for each field.
_help_text = {
    'project_title': 'The title of the project',
    'short_summary': 'This field is displayed in "overviews" such as the projects listing page.',
    'description': 'A free-form description of the plugin.',
    'sensitive': 'True if data is sensitive and cannot be revealed to the public.',
    'budget': 'Initial funding amount (USD)',
    'student_support': 'A project may have support from students.',
    'location': 'A park/location for a project',
    'fed_poc': 'federal point of contact',
    'pp_i': 'Partner Principle Investigator',
    'funding': 'The current/final funding amount',
    'start_date': 'Tentative start date of project',
    'end_date': 'Tentative end date of project',
    'discipline': 'The discipline related to the project',
    'type': 'Type of project implemented',
    'r_d': 'Research and Development fields',
    'tech_rep': 'Agreements Tech Representative if Partner:NPS is selected',
    'alt_coord': 'The Alternate Research Coordinator / CESU Representative',
    'src_of_funding': 'The source of the funding'
}


class Project(models.Model):

    def project_directory_path(self, filename):
        return 'projects/{0}/{1}'.format(str(self.id), filename)

    GRADUATE = 'GRAD'
    UNDERGRADUATE = 'UGRAD'
    BOTH = 'BOTH'
    NONE = 'NONE'
    UNKNOWN = 'UNKNOWN'

    YOUTH = 'YOUTH'
    VETS = 'VETS'


    DRAFTING = 'DRAFT'
    EXECUTED = 'EXEC'
    CLOSED = 'CLOSE'
    STUDENT_SUPPORT = (
        (GRADUATE, 'Graduate'),
        (UNDERGRADUATE, 'Undergraduate'),
        (BOTH, 'Graduate and Undergraduate'),
        (UNKNOWN, 'Unknown'),
        (NONE, 'None'),
    )
    VET_SUPPORT = (
        (YOUTH, 'Youth/Young Adults'),
        (BOTH, 'Graduate and Undergraduate'),
        (UNKNOWN, 'Unknown'),
        (NONE, 'None'),
    )
    STATUS = (
        (DRAFTING, 'Drafting'),
        (EXECUTED, 'Executed'),
        (CLOSED, 'Closed')
    )
    # Fields to be required: (Tentative)
    # TODO: Replace this as the unique field for a project
    p_num = models.IntegerField(verbose_name="P-Number", blank=True, default=0)
    project_title = models.CharField(max_length=500, unique=True, help_text=_help_text['project_title'])
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'])
    description = models.TextField(help_text=_help_text['description'], verbose_name="Description/Abstract")
    sensitive = models.BooleanField(default=False, help_text=_help_text['sensitive'])
    budget = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['budget'])
    student_support = models.CharField(max_length=5, choices=STUDENT_SUPPORT, default=NONE)
    vet_support = models.CharField(max_length=5, choices=STUDENT_SUPPORT, default=NONE,
                                   verbose_name="Youth/Veteran involvement")
    status = models.CharField(max_length=5, choices=STATUS, default=DRAFTING)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE,
                                related_name='partner', default=None)
    federal_agency = models.ForeignKey(FederalAgency, on_delete=models.CASCADE,
                                       related_name='federal_agency', default=None)
    cesu_unit = models.ForeignKey(CESUnit, on_delete=models.CASCADE,
                                  related_name='cesu_unit', default=None)
    location = models.CharField(max_length=500, help_text=_help_text['location'], blank=True)
    fed_poc = models.CharField(max_length=500, help_text=_help_text['fed_poc'], blank=True,
                               verbose_name="Federal Point of Contact")
    pp_i = models.CharField(max_length=500, help_text=_help_text['pp_i'], blank=True,
                            verbose_name="Partner Principle Investigator")
    funding = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['funding'], blank=True,
                                  default=0.00)
    tent_start_date = models.DateField(blank=True, default="2019-1-1", verbose_name="Tentative Start Date (YYYY/MM/DD)")
    tent_end_date = models.DateField(blank=True, default="2019-1-1", verbose_name="Tentative End Date (YYYY/MM/DD)")
    init_start_date = models.DateField(blank=True, default="2019-1-1",
                                       verbose_name="Project Initially received (YYYY/MM/DD)")
    comm_start_date = models.DateField(blank=True, default="2019-1-1",
                                       verbose_name="Date Review Comments Sent (YYYY/MM/DD)")
    task_agreement_start_date = models.DateField(blank=True, default="2019-1-1",
                                                 verbose_name="Date Task Agreement Approved (YYYY/MM/DD)")
    # TODO: Make this automatic whenever they change the status to EXEC
    exec_start_date = models.DateField(blank=True, default="2019-1-1",
                                       verbose_name="Date Executed (YYYY/MM/DD)")
    actual_start = models.DateField(blank=True, default="2019-1-1", verbose_name="Actual Start Date (YYYY/MM/DD)")
    actual_end = models.DateField(blank=True, default="2019-1-1", verbose_name="Actual Start Date (YYYY/MM/DD)")
    fiscal_year = models.DecimalField(blank=True, default=2019, max_digits=4, decimal_places=0, max_length=9999)
    discipline = models.CharField(max_length=500, help_text=_help_text['discipline'], blank=True)
    type = models.CharField(max_length=500, help_text=_help_text['type'], blank=True)
    r_d = models.CharField(max_length=500, help_text=_help_text['r_d'], blank=True,
                           verbose_name="Research & Development Type")
    final_report = models.BooleanField(verbose_name="Final Report", default=False)
    # TODO: If the sensitive field is checked then remove this field from the form. Splashes proj onto pub page
    perm_share = models.BooleanField(verbose_name="Permission to share", default=False)
    # Optional fields as follows:
    # TODO: If NPS is selected then this field should display
    tech_rep = models.CharField(max_length=500, help_text=_help_text['tech_rep'], blank=True,
                                verbose_name="Agreements Tech Representative")
    alt_coord = models.CharField(max_length=500, help_text=_help_text['alt_coord'], blank=True,
                                 verbose_name="Alternate Research Coordinator / CESU Representative")
    # TODO: If R & D is applicable include the following
    src_of_funding = models.CharField(max_length=500, help_text=_help_text['src_of_funding'], blank=True,
                                      verbose_name="Source of Funding")
    monitoring = models.BooleanField(default=False)
    sci_method = models.BooleanField(default=False)
    req_iacuc = models.BooleanField(verbose_name="Requires IACUC Review/ Concurrence", default=False)

    date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('summit.apps.projects:project-detail', args=[str(self.id)])

    def __str__(self):
        return self.project_title


class File(models.Model):
    # TODO: Read file in 'chunks' ---> https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    file_name = 'projects/' + str(project)
    file = models.FileField(blank=True, upload_to=file_name)

    def __str__(self):
        return file_name


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
