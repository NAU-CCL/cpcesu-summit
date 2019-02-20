from django.db import models

# Create your models here.
from summit.libs.models import AuditModel

from summit.libs.auth.models import UserProfile, UserGroup, get_all_user_groups


AUDIENCES = get_all_user_groups()

print(AUDIENCES)


class Document(AuditModel):
    authors = models.ManyToManyField(UserProfile)
    html_body = models.TextField(default='')
    is_published = models.BooleanField(default=False)
    groups = models.CharField(max_length=100, choices=AUDIENCES, default=0)


class Page(AuditModel):
    page_id = models.CharField(max_length=255)
    documents = models.ManyToManyField(Document)
