from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'seen')


admin.site.register(Notification, NotificationAdmin)
