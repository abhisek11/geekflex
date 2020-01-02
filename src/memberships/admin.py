from django.contrib import admin

from memberships.models import *
# Register your models here.
@admin.register(Membership)
class Membership(admin.ModelAdmin):
    list_display = [field.name for field in Membership._meta.fields]
    # search_fields = ('cu_user__username','cu_phone_no')

@admin.register(UserMembership)
class UserMembership(admin.ModelAdmin):
    list_display = [field.name for field in UserMembership._meta.fields]
    search_fields = ('user')
