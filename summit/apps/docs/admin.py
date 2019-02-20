from django.contrib import admin

from .models import Page, Document  # , Audience

# Register your models here.
admin.site.register(Page)
admin.site.register(Document)
# admin.site.register(Audience)
