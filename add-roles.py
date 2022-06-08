from summit.libs.auth.models import CESU
from summit.libs.auth.models import CESURole
from summit.libs.auth.models import User

summit = CESU.objects.get(id=1)
ex = CESU.objects.get(id=2)

CESURole.objects.all().delete()
for user in User.objects.all():
  new_role = CESURole.objects.get_or_create(user_id = user.id, cesu_id=summit.id)[0]
  new_role.role = 'USER'
  new_role.save()
  new_role = CESURole.objects.get_or_create(user_id = user.id, cesu_id=ex.id)[0]
  new_role.role = 'USER'
  new_role.save()