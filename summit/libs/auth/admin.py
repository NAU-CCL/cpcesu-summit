from django.contrib import admin
from django.contrib.auth.models import Permission

from summit.libs.auth.models import User


admin.site.register(User)
admin.site.register(Permission)

# Register your models here.
