from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group

import uuid

from summit.libs.models import AuditModel


class User(AbstractUser, AuditModel):
    full_name = models.CharField(max_length=300)
    first_name = None
    last_name = None
    external_id = models.CharField(max_length=100, unique=True, blank=False, default=uuid.uuid4)


class Permission(Permission):
    is_active = models.BooleanField(default=True)


class Group(Group):
    is_active = models.BooleanField(default=True)
