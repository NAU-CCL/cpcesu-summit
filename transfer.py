from summit.libs.auth.models import FederalAgency
from summit.libs.auth.models import Partner
from summit.libs.auth.models import CESU
from summit.libs.auth.models import CESUnit
from summit.libs.auth.models import Organization


for partner in Partner.objects.all():
	created_org = Organization.objects.create(id=partner.id, type='Federal Agency', name= partner.name, description= partner.description, logo= partner.avatar, contact='')

for agency in FederalAgency.objects.all():
	created_org = Organization.objects.create(id=agency.id, type='Federal Agency', name= agency.name, description= agency.description, logo= agency.avatar, contact='')

for cesu in CESUnit.objects.all():
	created_org = CESU.objects.create(id= cesu.id, name= cesu.name, description= cesu.description, logo= cesu.avatar, contact='')