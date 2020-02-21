from django.db import models
from django.contrib.auth.models import User
from datetime import date
import time


class AdminMenu(models.Model):
    name =  models.CharField( max_length=500,blank=True,null=True)
    url = models.CharField( max_length=500,blank=True,null=True)
    icon = models.CharField( max_length=500,blank=True,null=True)
    parent_id = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='admin_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='admin_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='admin_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'admin_menu'

class Role(models.Model):
    name =  models.CharField( max_length=500,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='role_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='role_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='role_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'role'

class RoleMenuMappingTable(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,blank=True,null=True)
    menu = models.ForeignKey(AdminMenu, on_delete=models.CASCADE,blank=True,null=True)
    is_create = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='role_menu_mapping_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='role_menu_mapping_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='role_menu_mapping_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'role_menu_mapping_table'

class RoleUserMappingTable(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='role_user_mapping_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='role_user_mapping_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='role_user_mapping_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'role_user_mapping_table'
