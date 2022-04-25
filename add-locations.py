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
Location.objects.all().delete()

# read line
with open('CPCESU_Summit-Data-Import_FINAL.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile, quotechar='"')
  for row in reader:

    proj = Project.objects.get(
      project_title = row['Project Title'],
      p_num = row['Award Number']
    )

    