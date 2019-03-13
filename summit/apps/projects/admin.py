from django.contrib import admin

from .models import Project, Notification, File


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'sensitive', 'short_summary')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'seen')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Notification, NotificationAdmin)
