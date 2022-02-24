from summit.apps.projects.models import Project
from summit.apps.projects.models import Location
from summit.libs.auth.models import CESU
from summit.libs.auth.models import Organization
from summit.libs.auth.models import UserProfile
import csv
from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

# only non user people are deleted because 
# deleting profiles that have users attached breaks the system
non_user_people = UserProfile.objects.exclude(user__isnull=False)
non_user_people.delete()
for user in UserProfile.objects.all():
  user.cesu = CESU.objects.get(id=1)
Project.objects.all().delete()
Location.objects.all().delete()
Organization.objects.all().delete()

# read line
with open('CPCESU_Summit-Data-Import_FINAL.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile, quotechar='"')
  for row in reader:
    is_before_22217 = False
    if (row['Start Date'] != ""):
      is_before_22217 = datetime.strptime(row['Start Date'], '%m/%d/%y') < datetime(2017, 2, 22)
    fed_agency = None
    project_partner = None
    project_location = None
    ppi = None
    techrep = None
    pm = None
    if (row['Federal Agency'] != ""):
      fed_agency = Organization.objects.get_or_create(
        name = row['Federal Agency'],
        type = 'Federal Agency'
      )[0]
    if (row['Partner'] != ""):
      project_partner = Organization.objects.get_or_create(
        name = row['Partner'],
        type = 'Partner'
      )[0]
    if (row['Location'] != ""):
      project_location = Location.objects.get_or_create(
        name = row['Location']
      )[0]
    if (row['Partner Principal Investigator First Name'] != ""):
      ppi = UserProfile.objects.get_or_create(
        first_name = row['Partner Principal Investigator First Name'],
        last_name = row['Partner Principal Investigator Last Name'],
        assigned_group = project_partner
      )[0]
    if (row['Federal Tech Rep First Name'] != ""):
      techrep = UserProfile.objects.get_or_create(
        first_name = row['Federal Tech Rep First Name'],
        last_name = row['Federal Tech Rep Last Name'],
        assigned_group = fed_agency
      )[0]
    if (row['Federal Project Lead First Name'] != ""):
      pm = UserProfile.objects.get_or_create(
        first_name = row['Federal Project Lead First Name'],
        last_name = row['Federal Project Lead Last Name'], 
        assigned_group = fed_agency
      )[0]
    Project.objects.create(
      cesu_unit = CESU.objects.get(id=1),
      federal_agency = fed_agency,
      partner = project_partner,
      fiscal_year = row['Fiscal Year'],
      p_num = row['Award Number'],
      local_num = row['Local Number'],
      location = project_location,
      project_title = row['Project Title'],
      type = row['Type'],
      discipline = row['Discipline'],
      
      budget = float(row['Initial Amount'].strip("$").replace(',','')) if row['Initial Amount'] != "" else 0,
      added_amount = float(row['Added Amount'].strip("$").replace(',','')) if row['Added Amount'] != "" else 0,
      total_amount = float(row['Total Amount'].strip("$").replace(',','')) if row['Total Amount'] != "" else 0,
      pp_i = ppi,
      project_manager = pm,
      tech_rep = techrep,
      num_of_students = 0 if row['Students Involved'] == "No" else 1,
      sensitive = False if row['Sensitive Data'] == "No" else True,
      description = row['Description'],
      notes = row['Notes'],
      init_start_date = datetime.strptime(row['Received Date'], '%m/%d/%y') if row['Received Date'] != "" else None,
      reviewed = datetime.strptime(row['Reviewed Date'], '%m/%d/%y') if row['Reviewed Date'] != "" else None,
      task_agreement_start_date = datetime.strptime(row['Approved Date'], '%m/%d/%y') if row['Approved Date'] != "" else None,
      tent_start_date = datetime.strptime(row['Start Date'], '%m/%d/%y') if row['Start Date'] != "" else None,
      tent_end_date = datetime.strptime(row['End Date'], '%m/%d/%y') if row['End Date'] != "" else None,
      status = "CLOSED" if is_before_22217 else "AWARDED",
      award_office = row['Awarding Office']
    )