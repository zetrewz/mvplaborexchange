from django.contrib import admin
from django.contrib.admin import ModelAdmin

from service.models import Application


# @admin.register(Application)
# class ApplicationAdmin(ModelAdmin):
#     list_display = ['resume', 'vacancy', 'applied']
admin.site.register(Application)
