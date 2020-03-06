from django.contrib import admin
from notifiyapp.models import *

@admin.register(NotifyTemplet)
class NotifyTemplet(admin.ModelAdmin):
    list_display = [field.name for field in NotifyTemplet._meta.fields]
