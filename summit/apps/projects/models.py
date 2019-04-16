from . import choices
from config.links import get_name
import datetime
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from summit.libs.auth.models import Partner, FederalAgency, CESUnit, UserProfile

# TODO: Create/Update help text for each field.
_help_text = choices.ProjectChoices.help_text


def get_directory_path(instance, filename):
    return 'projects/{0}/{1}'.format(instance.project.id, filename)


class Location(models.Model):
    name = models.TextField(max_length=255, unique=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('summit.apps.projects:location-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Project(models.Model):

    DISCIPLINE = choices.ProjectChoices.DISCIPLINE
    FIELD_OF_SCIENCE = choices.ProjectChoices.FIELD_OF_SCIENCE
    MOD_TYPE = choices.ProjectChoices.MOD_TYPE
    R_D_TYPE = choices.ProjectChoices.R_D_TYPE
    SOURCE_OF_FUNDING = choices.ProjectChoices.SOURCE_OF_FUNDING
    STATUS = choices.ProjectChoices.STATUS
    STUDENT_SUPPORT = choices.ProjectChoices.STUDENT_SUPPORT
    TYPE = choices.ProjectChoices.TYPE
    VET_SUPPORT = choices.ProjectChoices.VET_SUPPORT

    # Fields to be required: (Tentative)
    # TODO: Replace this as the unique field for a project
    budget = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['budget'])
    cesu_unit = models.ForeignKey(CESUnit, on_delete=models.CASCADE,
                                  related_name='cesu_unit', default=None, verbose_name="CESUnit")
    description = models.TextField(help_text=_help_text['description'], verbose_name="Abstract")
    discipline = models.CharField(max_length=20, choices=DISCIPLINE,
                                  help_text=_help_text['discipline'], blank=False,
                                  default=DISCIPLINE[0])
    federal_agency = models.ForeignKey(FederalAgency, on_delete=models.CASCADE,
                                       related_name='federal_agency', default=None)
    field_of_science = models.CharField(max_length=500, help_text=_help_text['field_of_science'], blank=True,
                                        verbose_name="Field of Science",
                                        choices=FIELD_OF_SCIENCE, default=FIELD_OF_SCIENCE[0])
    final_report = models.BooleanField(verbose_name="Final Report", default=False)
    fiscal_year = models.PositiveSmallIntegerField(blank=True, default=2019,
                                                   verbose_name="Fiscal Year")
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 related_name='location', default=None,
                                 verbose_name="Location", blank=True)
    init_start_date = models.DateField(blank=True, default="2019-1-1",
                                       verbose_name="Project Initially received (YYYY/MM/DD)")
    monitoring = models.BooleanField(default=False)
    notes = models.TextField(help_text=_help_text['notes'], blank=True)
    num_of_students = models.PositiveSmallIntegerField(blank=True, help_text=_help_text['num_of_students'],
                                                       default=0, verbose_name="Number of Students")
    p_num = models.CharField(verbose_name="P-Number", blank=True, max_length=500, help_text=_help_text['p_num'])
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='partner', default=None)
    pp_i = models.ForeignKey(UserProfile, on_delete=models.CASCADE, help_text=_help_text['pp_i'], blank=True,
                             verbose_name="Partner Principle Investigator", related_name='pp_i', default=None)
    project_manager = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                        verbose_name="Project Manager", blank=True,
                                        related_name='project_manager', default=None, null=True)
    project_title = models.CharField(max_length=500, unique=True, help_text=_help_text['project_title'])
    r_d = models.CharField(max_length=50, help_text=_help_text['r_d'],
                           blank=True, verbose_name="Research & Development Type",
                           choices=R_D_TYPE)
    sci_method = models.BooleanField(default=False)
    sensitive = models.BooleanField(default=False, help_text=_help_text['sensitive'])
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'],
                                     verbose_name="Short Description")
    src_of_funding = models.CharField(max_length=500, help_text=_help_text['src_of_funding'],
                                      blank=True, verbose_name="Source of Funding/Award Type",
                                      choices=SOURCE_OF_FUNDING, default=SOURCE_OF_FUNDING[0])
    staff_member = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Staff Member",
                                     blank=True, related_name='staff_member', default=None)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS[0])
    student_support = models.CharField(max_length=7, choices=STUDENT_SUPPORT, default=STUDENT_SUPPORT[0])
    tech_rep = models.ForeignKey(UserProfile, help_text=_help_text['tech_rep'], blank=True,
                                 verbose_name="Agreements Tech Representative")
    tent_end_date = models.DateField(blank=True, default="2019-1-1",
                                     verbose_name="Tentative End Date (YYYY/MM/DD)")
    tent_start_date = models.DateField(blank=True, default="2019-1-1",
                                       verbose_name="Tentative Start Date (YYYY/MM/DD)")
    type = models.CharField(max_length=50, choices=TYPE, help_text=_help_text['type'],
                            blank=False, verbose_name="Project Type")
    vet_support = models.CharField(max_length=5, choices=VET_SUPPORT, default=VET_SUPPORT[0],
                                   verbose_name="Youth/Veteran involvement")

# Fields that follow have not been added to the project create/edit forms
    fed_poc = models.CharField(max_length=500, help_text=_help_text['fed_poc'], blank=True,
                               verbose_name="Federal Point of Contact")

    funding = models.DecimalField(max_digits=12, decimal_places=2,
                                  help_text=_help_text['funding'], blank=True,default=0.00)
    comm_start_date = models.DateField(blank=True, default="2019-1-1", verbose_name="Review Comments Sent (YYYY/MM/DD)")
    task_agreement_start_date = models.DateField(blank=True, default="2019-1-1",
                                                 verbose_name="Date Task Agreement Approved (YYYY/MM/DD)")
    # TODO: Make this automatic whenever they change the status to EXEC
    exec_start_date = models.DateField(blank=True, default="2019-1-1",verbose_name="Date Executed (YYYY/MM/DD)")
    actual_start = models.DateField(blank=True, default="2019-1-1", verbose_name="Actual Start Date (YYYY/MM/DD)")
    actual_end = models.DateField(blank=True, default="2019-1-1", verbose_name="Actual Start Date (YYYY/MM/DD)")
    # TODO: If the sensitive field is checked then remove this field from the form. Splashes proj onto pub page
    perm_share = models.BooleanField(verbose_name="Permission to share", default=False)
    award_amt = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['award_amt'],
                                    blank=True, default=0.0)
    alt_coord = models.CharField(max_length=500, help_text=_help_text['alt_coord'], blank=True,
                                 verbose_name="Alternate Research Coordinator / CESU Representative")
    req_iacuc = models.BooleanField(verbose_name="Requires IACUC Review/ Concurrence", default=False)

    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('summit.apps.projects:project-detail', args=[str(self.id)])

    def __str__(self):
        return self.project_title


class Modification(models.Model):
    MOD_TYPE = choices.ProjectChoices.MOD_TYPE

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    mod_desc = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Description")
    mod_num = models.CharField(verbose_name="Modification #", max_length=500, help_text=_help_text['mod_num'],
                               blank=True, null=True)
    mod_type = models.CharField(max_length=50, verbose_name="Modification Type",
                                choices=MOD_TYPE, default=MOD_TYPE[0], null=True, blank=True)
    mod_notes = models.TextField(blank=True, verbose_name="Modification Notes")
    mod_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mod_approved = models.DateField(blank=True, default="2019-1-1",
                                    verbose_name="Approved (YYYY/MM/DD)")
    mod_executed = models.DateField(blank=True, default="2019-1-1",
                                    verbose_name="Executed (YYYY/MM/DD)")

    def __str__(self):
        return str(self.mod_num)


# TODO: Read file in 'chunks' ---> https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    file = models.FileField(blank=True, upload_to=get_directory_path, verbose_name="Select File(s)")

    def __str__(self):
        return str(self.file)


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
