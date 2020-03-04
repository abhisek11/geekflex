from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from django.conf import settings
from custom_exception_message import *
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from drf_extra_fields.fields import Base64ImageField # for image base 64
from django.db import transaction, IntegrityError
from adminpanel.models import *
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from threading import Thread  # for threading
import datetime
from videoservices.models import *
from adminpanel.views import *


class MenuAddViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    parent_id = serializers.IntegerField(required=False)
    class Meta:
        model=AdminMenu
        fields=('__all__')

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            name = validated_data.get('name')
            url= validated_data.get('url')
            icon= validated_data.get('icon')
            created_by=validated_data.get('created_by')
            owned_by=validated_data.get('owned_by')
            parent_id = validated_data.get('parent_id') if validated_data.get('parent_id') else 0

            with transaction.atomic():
                menu_add = AdminMenu.objects.create(name=name,url=url,parent_id=parent_id,icon=icon,
                                                    created_by=created_by,owned_by=owned_by)

                return validated_data

        except Exception as e:
            raise e

class RoleAddViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    menu_list = serializers.ListField(required=False)
    class Meta:
        model=Role
        fields=('__all__')

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            name = validated_data.get('name')
            menu_list = validated_data.get('menu_list')
            created_by=validated_data.get('created_by')
            owned_by=validated_data.get('owned_by')
            print("name",name,"menu_list",menu_list)
            with transaction.atomic():
                role_exist = Role.objects.filter(name__iexact=name)
                print("role_exist",role_exist)
                if not role_exist:
                    role_add = Role.objects.create(name=name,created_by=created_by,owned_by=owned_by)
                    for menu in menu_list:
                        print("menu['id']",menu['id'])
                        is_create=menu['permission']['is_create'] if 'is_create' in menu['permission'] else 0
                        is_read=menu['permission']['is_read'] if 'is_read' in menu['permission'] else 0
                        is_delete=menu['permission']['is_delete'] if 'is_delete' in menu['permission'] else 0
                        is_edit=menu['permission']['is_edit'] if 'is_edit' in menu['permission'] else 0

                        role_menu_mapping= RoleMenuMappingTable.objects.create(role=role_add,menu_id=menu['id'],
                                                                                is_create=is_create,
                                                                                is_read=is_read,
                                                                                is_delete=is_delete,
                                                                                is_edit=is_edit,
                                                                                created_by=created_by,owned_by=owned_by)
                    return validated_data
                else:
                    raise CustomAPIException(None,'Role cannot be duplicate',status_code=status.HTTP_200_OK)

        except Exception as e:
            raise e

class MenuListViewSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=AdminMenu
        fields=('id','name','parent_id')

class RoleListViewSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Role
        fields=('id','name')

class AdminUserCreateViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    username=serializers.CharField(required=False)
    role=serializers.CharField(required=False)
    firstname=serializers.CharField(required=False)
    lastname=serializers.CharField(required=False)
    groups =  serializers.ListField(required=False)
    user_permissions = serializers.ListField(required=False)
    user = serializers.DictField(required=False)
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model=User
        fields='__all__'

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            auth_provider = validated_data.get('auth_provider') if validated_data.get('auth_provider') else 'Kidsclub'
            created_by= validated_data.get('created_by')
            owned_by=validated_data.get('owned_by')
            with transaction.atomic():
                firstname= validated_data.get('firstname') if validated_data.get('firstname') else ""
                lastname= validated_data.get('lastname') if validated_data.get('lastname') else ""
                email= validated_data.get('email') if validated_data.get('email') else None
                password = validated_data.get('password') if validated_data.get('password') else None
                confirm_password = validated_data.get('confirm_password') if validated_data.get('confirm_password') else None
                role= validated_data.get('role') if validated_data.get('role') else ""
                if email is None or password is None:
                    custom_exception_message(self,None,"Please provide both email and password ")
                else:
                    if password == confirm_password:
                        print("pasword matched ")
                        # pwd = make_password(password)
                        if User.objects.filter(email = email).exists():
                            print("test user")
                            raise CustomAPIException(None,"Email ID already exist ",status_code=status.HTTP_409_CONFLICT)
                        else:
                            user= User.objects.create_user(username = email,email=email,
                                                                    first_name=firstname,last_name=lastname)
                            user.set_password(password)
                            # user.is_staff = True #for testing of user 
                            user.is_active = True
                            user.is_superuser=True
                            user.save()

                            user_road_mapping_create = RoleUserMappingTable.objects.create(user=user,role_id=role,
                                                            created_by=created_by,owned_by=owned_by)
                    else:
                        custom_exception_message(self,None,"Password did not matched")
                validated_data['is_active']=user.is_active
                validated_data['is_superuser']=user.is_superuser
                validated_data['user']={
                    'user_id':user.__dict__['id'],
                    'user_email':user.__dict__['email']
                }

                return validated_data

        except Exception as e:
            raise e


class AdminUserListViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    role=serializers.CharField(required=False)

    class Meta:
        model=User
        fields=('id','username','first_name','last_name','email','is_active','role','created_by','owned_by')

class MenuOnlyParentListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminMenu
        fields=('id','name')

class AppUserListViewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields='__all__'

class AppUserActivateViewSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=('id','first_name','last_name','email','is_active','is_superuser')

class VideoListViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    tags =  serializers.ListField(required=False)
    class Meta:
        model=Video
        fields=('__all__')
