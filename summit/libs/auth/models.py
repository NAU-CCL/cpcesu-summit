from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid

from summit.libs.models import AuditModel
#
# class User(AbstractUser, AuditModel):
#     full_name = models.CharField(max_length=300)
#     external_id = models.CharField(max_length=100,unique=True,blank=False,default=uuid.uuid4)
