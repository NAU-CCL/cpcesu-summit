from django.db import models

from summit.apps.projects.models import Project


class Notification(models.Model):
    TYPE_OPTIONS = (
        ('CHECKUP', 'Checkup'),
        ('NONE', 'None'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default='NONE')
    description = models.TextField(help_text="The specific details to the Notification, such as reason, instructions, \
    etc.")
    seen = models.BooleanField(default=False)

    #def mark_seen(self):
    #    self.seen = True

    def __str__(self):
        return self.description