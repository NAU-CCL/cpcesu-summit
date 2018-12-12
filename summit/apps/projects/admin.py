from django.contrib import admin

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'sensitive', 'short_summary')


admin.site.register(Project, ProjectAdmin)
