from django.contrib import admin
from . import models

admin.site.register(models.Activity)
admin.site.register(models.Flag)
admin.site.register(models.OpRecord)
