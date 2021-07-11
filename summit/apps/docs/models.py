from django.db import models

# Create your models here.
from summit.libs.models import AuditModel

from summit.libs.auth.models import UserProfile


class Document(AuditModel):
    # Added on_delete=models.DO_NOTHING since on_delete is now required
    created_by = models.ForeignKey(UserProfile, verbose_name="Created By", related_name='%(class)s_doc_created', on_delete=models.DO_NOTHING)
    last_edited_by = models.ForeignKey(UserProfile, verbose_name="Last Edited By", related_name='%(class)s_last_edit_by', on_delete=models.DO_NOTHING)

    page_id = models.CharField(max_length=255, unique=True, blank=False, verbose_name="Page ID")
    title = models.CharField(max_length=64, default="No Title")
    html_body = models.TextField(default='', verbose_name="Document Body")
    is_published = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
