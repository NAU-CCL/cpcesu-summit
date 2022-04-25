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
with open('agency_acronyms.csv',encoding='utf-8-sig', newline='') as csvfile:
  reader = csv.DictReader(csvfile, quotechar='"')
  for row in reader:
    
    if (row['Federal Agency'] != ""):
      org = Organization.objects.get_or_create(
        name = row['Federal Agency'],
      )[0]
      org.abbrv = row['Acronym']
      org.save()
      print(org.abbrv)

with open('partner_acronyms.csv',encoding='utf-8-sig', newline='') as csvfile:
  reader = csv.DictReader(csvfile, quotechar='"')
  for row in reader:
    
    if (row['Partner'] != ""):
      org = Organization.objects.get_or_create(
        name = row['Partner'],
      )[0]
      org.abbrv = row['Acronym']
      org.save()
      print(org.abbrv)