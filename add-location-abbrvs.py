from summit.apps.projects.models import Project
from summit.apps.projects.models import Location
from summit.libs.auth.models import CESU
from summit.libs.auth.models import Organization
from summit.libs.auth.models import UserProfile
import csv
from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

# read line
with open('location_acronyms.csv',encoding='utf-8-sig', newline='') as csvfile:
  reader = csv.DictReader(csvfile, quotechar='"')
  for row in reader:
    
    if (row['Location'] != ""):
      place = Location.objects.get_or_create(
        abbrv = row['Acronym'],
      )[0]
      place.name = row['Location']
      place.save()
      print(place.name)
