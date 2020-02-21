from django.shortcuts import render
from rest_framework import generics
from adminpanel.serializers import *
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.db import transaction, IntegrityError
from rest_framework.permissions import AllowAny
from knox.auth import TokenAuthentication
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from pagination import CSLimitOffestpagination, CSPageNumberPagination,OnOffPagination
from django_filters.rest_framework import DjangoFilterBackend
import collections
from videoservices.models import *
from rest_framework import mixins
from custom_decorator import *
from rest_framework.views import APIView
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from threading import Thread  # for threading
import datetime


class MenuAddView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = AdminMenu.objects.filter(is_deleted=False)
    serializer_class = MenuAddViewSerializer
    pagination_class = OnOffPagination

    def get_queryset(self):
        menu_id = self.request.query_params.get('menu_id', None)
        if menu_id:
            return self.queryset.filter(id=menu_id,is_deleted=False)
        else:
            return self.queryset

    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        menu_id = self.request.query_params.get('menu_id', None)
        method = self.request.query_params.get('method', None)
        updated_by=request.user
        with transaction.atomic():
            if method.lower() == 'edit':
                name=request.data['name'] if request.data['name'] else None
                url=request.data['url']  if request.data['url'] else None
                parent_id=request.data['parent_id']  if request.data['parent_id'] else 0
                menu_update = AdminMenu.objects.filter(id=menu_id,is_deleted=False).\
                                        update(name=name,url=url,parent_id=parent_id,updated_by=updated_by)
                if menu_update:
                    data = AdminMenu.objects.get(id=menu_id,is_deleted=False)
                    data.__dict__.pop('_state')
                    return Response({'results': data.__dict__,
                                        'msg': 'success',
                                        "request_status": 1})
                else:
                    return Response({'results': [],
                                    'msg': 'fail',
                                    "request_status": 0})
            
            elif method.lower() == 'delete':
                menu_update = AdminMenu.objects.filter(id=menu_id,is_deleted=False).\
                                        update(is_deleted=True)
                if menu_update:
                    return Response({'results':{
                                        'menu_id':menu_id ,
                                        },
                                        'msg': 'deleted successfully',
                                        "request_status": 1})
                else:
                    return Response({'results': [],
                                    'msg': 'fail to delete',
                                    "request_status": 0})

class RoleAddView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Role.objects.filter(is_deleted=False)
    serializer_class = RoleAddViewSerializer
    pagination_class = OnOffPagination

    def get_queryset(self):
        role_id = self.request.query_params.get('role_id', None)
        if role_id:
            return self.queryset.filter(id=role_id,is_deleted=False)
        else:
            return self.queryset

    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        response1 = response.data['results'] if 'results' in response.data else response.data
        menu_list=[]
        for data in response1:
            menu_data = RoleMenuMappingTable.objects.filter(role=data['id'],is_deleted=False)
            print("menu_data",menu_data)
            for m_p in menu_data:
                if m_p:
                    # menu_value = m_p.objects.values('menu','menu__name')
                    # permission_value = m_p.objects.values('is_create','is_read','is_delete','is_edit')
                   
                    menu_dict={
                        'id':m_p.menu.id,
                        'name':m_p.menu.name,
                        'permission':{
                            'is_create':m_p.is_create,
                            'is_read':m_p.is_read,
                            'is_delete':m_p.is_delete,
                            'is_edit':m_p.is_edit
                        }
                    }
                    menu_list.append(menu_dict)
            data['menu_list']=menu_list

        return response

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        role_id = self.request.query_params.get('role_id', None)
        method = self.request.query_params.get('method', None)
        updated_by=request.user
        with transaction.atomic():
            if method.lower() == 'edit':
                name=request.data['name'] if request.data['name'] else None
                menu_list=request.data['menu_list']
                previous_menu_items = RoleMenuMappingTable.objects.filter(role__name=name).values_list('menu',flat=True)
                print("previous_menu_items",previous_menu_items)
                deleted_menu_items = list(set(previous_menu_items)-set(menu_list))
                print("deleted_menu_items",deleted_menu_items)
                added_menu_items = list(set(menu_list)-set(previous_menu_items))
                print("added_menu_items",added_menu_items)
                delete_menu = RoleMenuMappingTable.objects.filter(role__name=name,menu__in=deleted_menu_items).update(is_deleted=True)
                
                for add_menu in added_menu_items:
                    added_menu = RoleMenuMappingTable.objects.create(role_id=role_id,menu_id=add_menu)
                role_update = Role.objects.filter(id=role_id,is_deleted=False).\
                                        update(name=name,updated_by=updated_by)
                if role_update:
                    data = Role.objects.get(id=role_id,is_deleted=False)
                    menu_data = RoleMenuMappingTable.objects.filter(role__name=name,is_deleted=False).values('menu','menu__name')
                    data.__dict__.pop('_state')
                    data.__dict__['menue_list_final'] = menu_data
                    return Response({'results': data.__dict__,
                                        'msg': 'success',
                                        "request_status": 1})
                else:
                    return Response({'results': [],
                                    'msg': 'fail',
                                    "request_status": 0})
            
            elif method.lower() == 'delete':
                role_update = Role.objects.filter(id=role_id,is_deleted=False).\
                                        update(is_deleted=True)
                if role_update:
                    return Response({'results':{
                                        'role_id':role_id ,
                                        },
                                        'msg': 'deleted successfully',
                                        "request_status": 1})
                else:
                    return Response({'results': [],
                                    'msg': 'fail to delete',
                                    "request_status": 0})


class MenuListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = AdminMenu.objects.filter(~Q(parent_id=0),is_deleted=False)
    serializer_class = MenuListViewSerializer

    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        menu_list = []
        for data in response.data:
            parent_details = AdminMenu.objects.filter(id=data['parent_id']).values('id','name')
            if parent_details:
                data_dict = {
                    "id":data['id'],
                    "name":data['name'],
                    "parent_details":parent_details[0]
                }
            else:
                data_dict = {
                    "id":data['id'],
                    "name":data['name'],
                }
            menu_list.append(data_dict)
        
        if len(menu_list)>0:
            return Response({'request_status':1,
                                'results':{
                                    'menu_list':menu_list,
                                    'msg':'success'
                                    },
                                },
                                status=status.HTTP_200_OK)
        else:
            return Response({'request_status':0,
                                'results':{
                                    'menu_list':[],
                                    'msg':'No Data Found'
                                    },
                                },
                                status=status.HTTP_200_OK)

class RoleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Role.objects.filter(is_deleted=False)
    serializer_class = RoleListViewSerializer

    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        role_list = []
        for data in response.data:
            data_dict = {
                "id":data['id'],
                "name":data['name'],
            }
            role_list.append(data_dict)
        
        if len(role_list)>0:
            return Response({'request_status':1,
                                'results':{
                                    'role_list':role_list,
                                    'msg':'success'
                                    },
                                },
                                status=status.HTTP_200_OK)
        else:
            return Response({'request_status':0,
                                'results':{
                                    'role_list':[],
                                    'msg':'No Data Found'
                                    },
                                },
                                status=status.HTTP_200_OK)


class AdminUserCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = AdminUserCreateViewSerializer

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)


class AdminUserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = AdminUserListViewSerializer
    pagination_class = OnOffPagination

    def get_queryset(self):
        user_id = self.request.user.id
        if user_id:
            print("user_id",user_id)
            return self.queryset.exclude(id=user_id).filter(is_superuser=True)
        else:
            return self.queryset.filter(is_superuser=True)

    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        response1 = response.data['results'] if 'results' in response.data else response.data
        for data in response1:
            data['role'] = RoleUserMappingTable.objects.filter(user=data['id']).values('role__id','role__name')
        
        return response

