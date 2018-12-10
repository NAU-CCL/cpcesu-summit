from django.db import models


class AuditModel(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True
