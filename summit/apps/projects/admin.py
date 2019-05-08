from django.contrib import admin

from .models import Project, File, Location, Modification, ModFile


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'sensitive', 'short_summary')


class FileAdmin(admin.ModelAdmin):
    list_display = ('project', 'file')


admin.site.register(Project)
admin.site.register(File)
admin.site.register(Modification)
admin.site.register(ModFile)
admin.site.register(Location)
