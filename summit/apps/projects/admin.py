from django.contrib import admin

from .models import Project, Notification, File
from simple_history.admin import SimpleHistoryAdmin


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'sensitive', 'short_summary')


class FileAdmin(admin.ModelAdmin):
    list_display = ('project', 'file')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'seen')


admin.site.register(Project, SimpleHistoryAdmin)
admin.site.register(File)
admin.site.register(Notification, NotificationAdmin)
