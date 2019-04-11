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
_help_text = {
    'p_num': 'Project number. Sometimes not received.',
    'project_title': 'The title of the project',
    'short_summary': 'This field is displayed in "overviews" such as the projects listing page.',
    'description': 'A free-form description of the plugin.',
    'sensitive': 'True if data is sensitive and cannot be revealed to the public.',
    'budget': 'Initial funding amount (USD)',
    'student_support': 'A project may have support from students.',
    'num_of_students': 'Number of students participating in student support.',
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
    'src_of_funding': 'The source of the funding',
    'award_amt': 'The amount that was awarded',
    'field_of_science': 'A specific field of science for the project.',
    'notes': 'General details or specifics that are worth writing down',
    'mod_num': 'An identification for the specific modification made.'
}


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

    GRADUATE = 'GRAD'
    UNDERGRADUATE = 'UGRAD'
    BOTH = 'BOTH'
    NONE = 'NONE'
    UNKNOWN = 'UNKNOWN'

    YOUTH = 'YOUTH'
    VETS = 'VETS'

    DRAFTING = 'DRAFT'
    EXECUTED = 'EXECUTED'
    CLOSED = 'CLOSED'

    NATURAL = 'NATURAL'
    CULTURAL = 'CULTURAL'
    SOCIAL = 'SOCIAL'
    INTERDISCIPLINARY = 'INTERDISCIPLINARY'

    EDUCATION = 'EDUCATION'
    RESEARCH = 'RESEARCH'
    TECHNICAL = 'TECHNICAL'
    ASSISTANCE = 'ASSISTANCE'

    PARK = 'PARK'
    REGION = 'REGION'
    SOURCE = 'SOURCE'
    PROGRAM = 'PROGRAM'
    OTHER_PROJECT_SOURCE = 'OTHER_PROJECT_SOURCE'
    REA_FEE_80 = 'REA_FEE_80'
    REA_FEE_20 = 'REA_FEE_20'
    OTHER_NPS_SOURCE = 'OTHER_NPS_SOURCE'
    OTHER = 'OTHER'

    NA = 'NA'
    APPLIED_RESEARCH = 'APPLIED_RESEARCH'
    BASIC_RESEARCH = 'BASIC_RESEARCH'
    R_D = 'R_D'
    DEVELOPMENT = 'DEVELOPMENT'

    ENVIRO_SCI = 'ENVIRO_SCI'
    LIFE_SCI = 'LIFE_SCI'
    MATH_CS = 'MATH_CS'
    PHYSICAL_SC = 'PHYSICAL_SC'
    SOCIAL_SC = 'SOCIAL_SC'

    FUNDED = 'FUNDED'
    NO_COST = 'NO-COST'
    ADMIN = 'ADMIN'
    FUNDED_EXT = 'FUNDED_EXT'
    FUNDED_ADMIN = 'FUNDED_ADMIN'
    NO_COST_EXT_ADMIN = 'NO_COST_EXT_ADMIN'
    STUDENT_SUPPORT = (
        (NONE, 'None'),
        (GRADUATE, 'Graduate'),
        (UNDERGRADUATE, 'Undergraduate'),
        (BOTH, 'Graduate and Undergraduate'),
        (UNKNOWN, 'Unknown'),
    )
    VET_SUPPORT = (
        (NONE, 'None'),
        (YOUTH, 'Youth/Young Adults'),
        (VETS, 'Veterans'),
        (BOTH, 'Youth/Young Adults and Veterans'),
    )
    STATUS = (
        (DRAFTING, 'Drafting'),
        (EXECUTED, 'Executed'),
        (CLOSED, 'Closed')
    )
    DISCIPLINE = (
        (NONE, 'None'),
        (NATURAL, 'Natural'),
        (CULTURAL, 'Cultural'),
        (SOCIAL, 'Social'),
        (INTERDISCIPLINARY, 'Interdisciplinary')
    )
    TYPE = (
        (NONE, 'None'),
        (EDUCATION, 'Education'),
        (RESEARCH, 'Research'),
        (TECHNICAL, 'Technical'),
        (ASSISTANCE, 'Assistance')
    )
    SOURCE_OF_FUNDING = (
        (NONE, 'None'),
        (PARK, 'Park Base'),
        (REGION, 'Region Base'),
        (SOURCE, 'NR Projcet Fund Source'),
        (PROGRAM, 'I&M Program'),
        (OTHER_PROJECT_SOURCE, 'Other Service-wide Project Source'),
        (REA_FEE_80, '80% REA Fee'),
        (REA_FEE_20, '20% REA Fee'),
        (OTHER_NPS_SOURCE, 'Other NPS Appropriated Source'),
        (OTHER, 'OTHER-non-NPS')
    )
    R_D_TYPE = (
        (NA, 'NA (TA or Educ)'),
        (APPLIED_RESEARCH, 'Applied Research'),
        (BASIC_RESEARCH, 'Basic Research'),
        (R_D, 'Research and Development'),
        (DEVELOPMENT, 'Development')
    )
    FIELD_OF_SCIENCE = (
        (NONE, 'None'),
        (ENVIRO_SCI, 'Environmental Sciences'),
        (LIFE_SCI, 'Life Sciences'),
        (MATH_CS, 'Mathematics and Computer Sciences'),
        (PHYSICAL_SC, 'Physical Sciences'),
        (SOCIAL_SC, 'Social Sciences')
    )
    MOD_TYPE = (
        (NONE, 'None'),
        (FUNDED, 'FUNDED'),
        (NO_COST, 'NO-COST'),
        (ADMIN, 'ADMIN'),
        (FUNDED_EXT, 'FUNDED_EXT'),
        (FUNDED_ADMIN, 'FUNDED_ADMIN'),
        (NO_COST_EXT_ADMIN, 'NO_COST_EXT_ADMIN')
    )
    # Fields to be required: (Tentative)
    # TODO: Replace this as the unique field for a project
    budget = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['budget'])
    cesu_unit = models.ForeignKey(CESUnit, on_delete=models.CASCADE,
                                  related_name='cesu_unit', default=None, verbose_name="CESUnit")
    description = models.TextField(help_text=_help_text['description'], verbose_name="Abstract")
    discipline = models.CharField(max_length=20, choices=DISCIPLINE, help_text=_help_text['discipline'],
                                  blank=False, default=NONE)
    federal_agency = models.ForeignKey(FederalAgency, on_delete=models.CASCADE,
                                       related_name='federal_agency', default=None)
    field_of_science = models.CharField(max_length=500, help_text=_help_text['field_of_science'], blank=True,
                                        verbose_name="Source of Funding/Award Type", choices=FIELD_OF_SCIENCE,
                                        default=NONE)
    final_report = models.BooleanField(verbose_name="Final Report", default=False)
    fiscal_year = models.PositiveSmallIntegerField(blank=True, default=2019,
                                                   verbose_name="Fiscal Year")
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 related_name='location', default=None,
                                 verbose_name="Location", blank=True)
    init_start_date = models.DateField(blank=True, default="2019-1-1",
                                       verbose_name="Project Initially received (YYYY/MM/DD)")
    mod_desc = models.TextField(max_length=1000, blank=True, null=True)
    mod_num = models.CharField(verbose_name="Modification #", max_length=500, help_text=_help_text['mod_num'],
                               blank=True, null=True)
    mod_type = models.CharField(max_length=50, verbose_name="Modification Type", choices=MOD_TYPE, default=NONE, null=True, blank=True)
    monitoring = models.BooleanField(default=False)
    notes = models.TextField(help_text=_help_text['notes'], blank=True)
    num_of_students = models.PositiveSmallIntegerField(blank=True, help_text=_help_text['num_of_students'],
                                                       default=0, verbose_name="Number of Students")
    p_num = models.CharField(verbose_name="P-Number", blank=True, max_length=500, help_text=_help_text['p_num'])
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='partner', default=None)
    pp_i = models.ForeignKey(UserProfile, on_delete=models.CASCADE, help_text=_help_text['pp_i'], blank=True, verbose_name="Partner Principle Investigator", related_name='pp_i', default=None)
    project_manager = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                        verbose_name="Project Manager", blank=True,
                                        related_name='project_manager', default=None, null=True)
    project_title = models.CharField(max_length=500, unique=True, help_text=_help_text['project_title'])
    r_d = models.CharField(max_length=50, help_text=_help_text['r_d'], blank=True, verbose_name="Research & Development Type", choices=R_D_TYPE)
    sci_method = models.BooleanField(default=False)
    sensitive = models.BooleanField(default=False, help_text=_help_text['sensitive'])
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'], verbose_name="Short Description")
    src_of_funding = models.CharField(max_length=500, help_text=_help_text['src_of_funding'], blank=True, verbose_name="Source of Funding/Award Type", choices=SOURCE_OF_FUNDING, default=NONE)
    staff_member = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Staff Member", blank=True, related_name='staff_member', default=None)
    status = models.CharField(max_length=20, choices=STATUS, default=DRAFTING)
    student_support = models.CharField(max_length=7, choices=STUDENT_SUPPORT, default=NONE)
    tech_rep = models.ForeignKey(UserProfile, help_text=_help_text['tech_rep'], blank=True, verbose_name="Agreements Tech Representative")
    tent_end_date = models.DateField(blank=True, default="2019-1-1", verbose_name="Tentative End Date (YYYY/MM/DD)")
    tent_start_date = models.DateField(blank=True, default="2019-1-1", verbose_name="Tentative Start Date (YYYY/MM/DD)")
    type = models.CharField(max_length=50, choices=TYPE, help_text=_help_text['type'], blank=False, verbose_name="Project Type")
    vet_support = models.CharField(max_length=5, choices=VET_SUPPORT, default=NONE, verbose_name="Youth/Veteran involvement")

# Fields that follow have not been added to the project create/edit forms
    fed_poc = models.CharField(max_length=500, help_text=_help_text['fed_poc'], blank=True, verbose_name="Federal Point of Contact")

    funding = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['funding'], blank=True,default=0.00)
    comm_start_date = models.DateField(blank=True, default="2019-1-1", verbose_name="Review Comments Sent (YYYY/MM/DD)")
    task_agreement_start_date = models.DateField(blank=True, default="2019-1-1", verbose_name="Date Task Agreement Approved (YYYY/MM/DD)")
    # TODO: Make this automatic whenever they change the status to EXEC
    exec_start_date = models.DateField(blank=True, default="2019-1-1",verbose_name="Date Executed (YYYY/MM/DD)")
    actual_start = models.DateField(blank=True, default="2019-1-1", verbose_name="Actual Start Date (YYYY/MM/DD)")
    actual_end = models.DateField(blank=True, default="2019-1-1", verbose_name="Actual Start Date (YYYY/MM/DD)")
    # TODO: If the sensitive field is checked then remove this field from the form. Splashes proj onto pub page
    perm_share = models.BooleanField(verbose_name="Permission to share", default=False)
    award_amt = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['award_amt'],  blank=True, default=0.0)
    alt_coord = models.CharField(max_length=500, help_text=_help_text['alt_coord'], blank=True, verbose_name="Alternate Research Coordinator / CESU Representative")
    req_iacuc = models.BooleanField(verbose_name="Requires IACUC Review/ Concurrence", default=False)

    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('summit.apps.projects:project-detail', args=[str(self.id)])

    def __str__(self):
        return self.project_title


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
