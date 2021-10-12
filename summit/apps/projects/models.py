from decimal import Decimal

from . import choices

from django.db import models

from summit.libs.auth.models import Partner, FederalAgency, CESUnit, UserProfile
from summit.libs.models import AuditModel

# TODO: Create/Update help text for each field.
_help_text = choices.ProjectChoices.help_text


def get_directory_path(instance, filename):
    if instance.id is None:
        return 'autofill/{0}'.format(filename)
    else:
        return 'projects/{0}/{1}'.format(instance.project.id, filename)


def get_mod_directory_path(instance, filename):
    return 'projects/{0}/{1}'.format(instance.id, filename)


class Location(models.Model):
    abbrv = models.TextField(max_length=64, blank=True, null=True)
    name = models.TextField(max_length=255, unique=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('summit.apps.projects:location_detail', args=[str(self.id)])

    def __str__(self):
        if self.abbrv:
            return self.name
        else:
            return self.name


from django.core.validators import MaxValueValidator, MinValueValidator


class Project(AuditModel):
    AWARD_OFFICE = choices.ProjectChoices.AWARD_OFFICE
    DISCIPLINE = choices.ProjectChoices.DISCIPLINE
    FIELD_OF_SCIENCE = choices.ProjectChoices.FIELD_OF_SCIENCE
    FIELD_OF_SCIENCE_SUB = choices.ProjectChoices.FIELD_OF_SCIENCE_SUB
    MOD_TYPE = choices.ProjectChoices.MOD_TYPE
    R_D_TYPE = choices.ProjectChoices.R_D_TYPE
    SOURCE_OF_FUNDING = choices.ProjectChoices.SOURCE_OF_FUNDING
    STATUS = choices.ProjectChoices.STATUS
    STUDENT_SUPPORT = choices.ProjectChoices.STUDENT_SUPPORT
    TYPE = choices.ProjectChoices.TYPE
    YOUTH_VETS = choices.ProjectChoices.YOUTH_VETS

    # Fields to be required: (Tentative)
    award_office = models.CharField(choices=AWARD_OFFICE, max_length=10, blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['budget'], blank=True, null=True,
                                 verbose_name="Initial", default=0, validators=[MinValueValidator(Decimal(0.00)), MaxValueValidator(Decimal('9999999.99'))])
    cesu_unit = models.ForeignKey(CESUnit, on_delete=models.SET_NULL,
                                  related_name='cesu_unit', default=None, verbose_name="CESUnit", blank=True, null=True)
    description = models.TextField(help_text=_help_text['description'], verbose_name="Abstract/Description", blank=True)
    discipline = models.CharField(max_length=21, choices=DISCIPLINE,
                                  help_text=_help_text['discipline'], blank=True,
                                  default=DISCIPLINE[0][0])
    exec_start_date = models.DateField(blank=True, null=True, default=None, verbose_name="Executed")
    federal_agency = models.ForeignKey(FederalAgency, on_delete=models.SET_NULL,
                                       related_name='federal_agency', default=None,
                                       blank=True, null=True, verbose_name="Agency")
    field_of_science = models.CharField(max_length=500, help_text=_help_text['field_of_science'], blank=True,
                                        verbose_name="Field of Science",
                                        choices=FIELD_OF_SCIENCE, default=FIELD_OF_SCIENCE[0][0])
    final_report = models.BooleanField(verbose_name="Final Report", default=False, blank=True)
    fiscal_year = models.PositiveSmallIntegerField(null=True, blank=True, default=2021,
                                                   verbose_name="Fiscal Year")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                 related_name='location', default=None,
                                 verbose_name="Place", blank=True, null=True)
    init_start_date = models.DateField(blank=True, default=None, null=True,
                                       verbose_name="Project Initially Received")
    monitoring = models.BooleanField(default=False)
    notes = models.TextField(help_text=_help_text['notes'], blank=True)
    num_of_students = models.PositiveSmallIntegerField(blank=True, help_text=_help_text['num_of_students'],
                                                       default=0, verbose_name="Number of Students")
    p_num = models.CharField(verbose_name="Award #", blank=True, max_length=500, help_text=_help_text['p_num'],
                             null=True)
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, related_name='partner', default=None, blank=True,
                                null=True)
    pp_i = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, help_text=_help_text['pp_i'], blank=True,
                             verbose_name="Partner Principle Investigator", related_name='pp_i', default=None,
                             null=True)
    project_manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                        verbose_name="Agency Project Manager", blank=True,
                                        related_name='project_manager', default=None, null=True)
    project_title = models.CharField(max_length=500, help_text=_help_text['project_title'], blank=True, null=True)
    r_d = models.CharField(max_length=50, help_text=_help_text['r_d'],
                           blank=True, verbose_name="Research & Development Type",
                           choices=R_D_TYPE)
    reviewed = models.DateField(null=True, blank=True, default=None)
    sci_method = models.BooleanField(default=False, blank=True)
    sensitive = models.BooleanField(default=False, help_text=_help_text['sensitive'],
                                    verbose_name="Sensitive", blank=True)
    short_summary = models.CharField(max_length=500, help_text=_help_text['short_summary'],
                                     verbose_name="Short Description", blank=True)
    src_of_funding = models.CharField(max_length=500, help_text=_help_text['src_of_funding'],
                                      blank=True, verbose_name="Source of Funding",
                                      choices=SOURCE_OF_FUNDING, default=SOURCE_OF_FUNDING[0][0])
    staff_member = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, verbose_name="Staff Member",
                                     blank=True, related_name='staff_member', default=None, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0], blank=True)
    last_status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0], blank=True)

    # I got an error "__init__() missing 1 required positional argument: 'on_delete'" 
    # so I added on_delete=models.SET_NULL since that is what other foreign keys in here use
    tech_rep = models.ForeignKey(UserProfile, help_text=_help_text['tech_rep'], blank=True,
                                 verbose_name="Agreements Tech Representative", on_delete=models.SET_NULL, null=True)
    tent_end_date = models.DateField(blank=True, default=None, null=True,
                                     verbose_name="Tentative End Date")
    tent_start_date = models.DateField(blank=True, default=None, null=True,
                                       verbose_name="Tentative Start Date")
    type = models.CharField(max_length=50, choices=TYPE, help_text=_help_text['type'],
                            blank=True, verbose_name="Project Type")

# Fields that follow have not been added to the project create/edit forms
    fed_poc = models.CharField(max_length=500, help_text=_help_text['fed_poc'], blank=True,
                               verbose_name="Federal Point of Contact")

    funding = models.DecimalField(max_digits=12, decimal_places=2,
                                  help_text=_help_text['funding'], blank=True, default=0.00)
    comm_start_date = models.DateField(blank=True, default=None, null=True,  verbose_name="Review Comments Sent")
    task_agreement_start_date = models.DateField(blank=True, default=None, null=True,
                                                 verbose_name="Approved")
    # TODO: Make this automatic whenever they change the status to EXEC
    actual_start = models.DateField(blank=True, default=None, null=True,  verbose_name="Actual Start Date")
    actual_end = models.DateField(blank=True, default=None, null=True,  verbose_name="Actual Start Date")
    # TODO: If the sensitive field is checked then remove this field from the form. Splashes proj onto pub page
    perm_share = models.BooleanField(verbose_name="Permission to share", default=False, blank=True)
    award_amt = models.DecimalField(max_digits=12, decimal_places=2, help_text=_help_text['award_amt'],
                                    blank=True, default=0.0)
    alt_coord = models.CharField(max_length=500, help_text=_help_text['alt_coord'], blank=True,
                                 verbose_name="Alternate Research Coordinator / CESU Representative")

    req_iacuc = models.BooleanField(verbose_name="Requires IACUC Review/ Concurrence", default=False, blank=True)
    youth_vets = models.CharField(choices=YOUTH_VETS, max_length=500, verbose_name="Youth/Vets", default=YOUTH_VETS[0])
    field_of_science_sub = models.CharField(choices=FIELD_OF_SCIENCE_SUB, max_length=100,
                                            blank=True, null=True, verbose_name="Sub-Fields (Field of Science)",
                                            default=FIELD_OF_SCIENCE_SUB[0][0])

    job_id = models.CharField(max_length=500, blank=True, null=True)

    # LEGACY FIELDS
    # Somewhat bad practice to apply to ALL projects, but will be necessary to bring in the old data
    legacy_award_number = models.TextField(verbose_name="Legacy - Award Number", default='')
    legacy_match_amount = models.TextField(verbose_name="Legacy - Match Amount", default='')
    legacy_ca_account_number = models.TextField(verbose_name="Legacy - CA Account Number", default='')
    legacy_account_number = models.TextField(verbose_name="Legacy - Account Number", default='')
    legacy_area_org = models.TextField(verbose_name="Legacy - Area/Org", default='')
    legacy_pwe = models.TextField(verbose_name="Legacy - PWE", default='')
    legacy_project_products = models.TextField(verbose_name="Legacy - Project Products", default='')
    legacy_received_report_date = models.TextField(verbose_name="Legacy - Received Report Date", default='')
    legacy_sent_to_tic = models.TextField(verbose_name="Legacy - Sent to TIC", default='')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('summit.apps.projects:project_detail', args=[str(self.id)])

    def __str__(self):
        if self.project_title is None or len(self.project_title) > 0:
            return "No Title"
        else:
            return self.project_title


class Modification(models.Model):
    MOD_TYPE = choices.ProjectChoices.MOD_TYPE
    STATUS = choices.ProjectChoices.STATUS

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    mod_desc = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Description")
    mod_num = models.CharField(verbose_name="Modification #", max_length=500, help_text=_help_text['mod_num'],
                               blank=False, null=True)
    mod_status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0], blank=True)
    mod_type = models.CharField(max_length=50, verbose_name="Modification Type",
                                choices=MOD_TYPE, default=MOD_TYPE[0], null=True, blank=True)
    mod_notes = models.TextField(blank=True, verbose_name="Modification Notes")
    mod_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    mod_approved = models.DateField(blank=True, null=True, verbose_name="Approved")
    mod_executed = models.DateField(blank=True, null=True, verbose_name="Executed")
    mod_extension = models.DateField(blank=True, null=True, verbose_name="Extension")

    def __str__(self):
        return str(self.mod_num)


# TODO: Read file in 'chunks' ---> https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/
class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    file = models.FileField(blank=True, upload_to=get_directory_path, verbose_name="Select File(s)")

    def __str__(self):
        return str.rsplit(str(self.file), sep='/', maxsplit=1)


class ModFile(models.Model):
    modification = models.ForeignKey(Modification, on_delete=models.SET_NULL, null=True)
    file = models.FileField(blank=True, upload_to=get_mod_directory_path, verbose_name="Select File(s)")

    def __str__(self):
        return str.rsplit(str(self.file), sep='/', maxsplit=1)
