from django.contrib import admin
from adminpanel.models import *

# Register your models here.
@admin.register(AdminMenu)
class AdminMenu(admin.ModelAdmin):
    list_display = [field.name for field in AdminMenu._meta.fields]

@admin.register(Role)
class Role(admin.ModelAdmin):
    list_display = [field.name for field in Role._meta.fields]

@admin.register(RoleMenuMappingTable)
class RoleMenuMappingTable(admin.ModelAdmin):
    list_display = [field.name for field in RoleMenuMappingTable._meta.fields]


@admin.register(RoleUserMappingTable)
class RoleUserMappingTable(admin.ModelAdmin):
    list_display = [field.name for field in RoleUserMappingTable._meta.fields]