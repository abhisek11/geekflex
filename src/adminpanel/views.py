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
                icon=request.data['icon']  if request.data['icon'] else None
                parent_id=request.data['parent_id']  if request.data['parent_id'] else 0
                menu_update = AdminMenu.objects.filter(id=menu_id,is_deleted=False).\
                                        update(name=name,url=url,parent_id=parent_id,icon=icon,updated_by=updated_by)
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

        parent_menu_list = AdminMenu.objects.filter(~Q(parent_id=0),is_deleted=False).values_list('parent_id',flat=True).distinct()
        stand_alon_parents = AdminMenu.objects.filter(~Q(id__in=parent_menu_list),parent_id=0,is_deleted=False).values('id','name')
        
        print("parent_menu_list",parent_menu_list)
        print("stand_alon_parents",stand_alon_parents)
        for s_data in stand_alon_parents:
            menu_list.append(s_data)
        # for s_data in stand_alon_parents:
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


class MenuOnlyParentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = AdminMenu.objects.filter(parent_id=0,is_deleted=False)
    serializer_class = MenuOnlyParentListViewSerializer
    pagination_class = OnOffPagination

    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)


class AppUserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = AppUserListViewSerializer
    pagination_class = OnOffPagination
    

    def get_queryset(self):
        account = self.request.query_params.get('account', None)
        search = self.request.query_params.get('search', None)
        filter={}
        if account:
            filter['account']=account
        #     print("account",account)
        #     return self.queryset.filter(account=account)
        # else:
        #     return self.queryset
        
        if search :
            search_data = list(map(str,search.split(" ")))
            print("This is if condition entry")
            if len(search.split(" "))>0 and len(search.split(" "))<2:
                print("length 1 hai ")
                queryset = self.queryset.filter((Q(firstname__icontains=search_data[0])|Q(lastname__icontains=search_data[0])),
                                                is_deleted=False,**filter)                            
                return queryset
            elif len(search.split(" "))>1:
                print("length 2 hai ")
                queryset = self.queryset.filter((Q(firstname__icontains=search_data[0]) & Q(lastname__icontains=search_data[1])),
                                                is_deleted=False,**filter)
                return queryset                

        else:
            queryset = self.queryset.filter(is_deleted=False,**filter)
            return queryset


    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        response1 = response.data['results'] if 'results' in response.data else response.data
        data_list=[] 
        for data in response1:
            print("data['account']",data['account'])
            if data['account'].lower() != 'company':
                if data['account'].lower() != 'parent':
                    data_dict={
                        'id':data['id'],
                        'user_id':data['user'],
                        'firstname':data['firstname'],
                        'lastname':data['lastname'],
                        'account':data['account'],
                        'is_active':User.objects.get(id=data['user']).is_active,
                        'regester_date':data['created_at'],
                    } 
                    data_list.append(data_dict)
                else:
                    data_dict={
                        'id':data['id'],
                        'user_id':data['user'],
                        'firstname':data['firstname'],
                        'lastname':data['lastname'],
                        'account':data['account'],
                        'is_active':User.objects.get(id=data['user']).is_active,
                        'regester_date':data['created_at'],
                    } 
                    child_data = SubChildProfile.objects.filter(profile=data['id'],is_deleted=False).values('firstname','lastname')
                    data_dict['children']=child_data
                    data_list.append(data_dict)
            else:
                data_dict={
                        'id':data['id'],
                        'user_id':data['user'],
                        'company_name':data['company_name'],
                        'account':data['account'],
                        'is_active':User.objects.get(id=data['user']).is_active,
                        'regester_date':data['created_at'],
                    } 
                data_list.append(data_dict)

            response.data['results']=data_list
        print("data_list",data_list)
        return response


class AppUserActivateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = AppUserActivateViewSerializer


    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super(self.__class__,self).put(request, *args, **kwargs)

class VideoListView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Video.objects.filter(is_deleted=False)
    serializer_class = VideoListViewSerializer
    pagination_class = OnOffPagination

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if search :
            queryset = self.queryset.filter(title__icontains=search,is_deleted=False).order_by('title')                           
            return queryset                

        else:
            queryset = self.queryset.filter(is_deleted=False).order_by('title')
            return queryset



    @response_modify_decorator_list_or_get_after_execution_for_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        for data in response.data['results']:
            link_list = []
            thumbnail = VideoThumbnailDocuments.objects.filter(video=data['id'],is_deleted=False)
            for link in thumbnail:
                link_list.append(request.build_absolute_uri(link.thumbnail.url))
            
            data['thumbnail_stack']=link_list
            channel_details = Profile.objects.get(id=data['channel'])

            if channel_details.account !='Company':
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'firstname':channel_details.firstname,
                    'lastname': channel_details.lastname,
                    'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count(),
                    'verified':channel_details.verified,
                    
                }
            else:
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'company_name': channel_details.company_name,
                    'address': channel_details.address,
                    'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count(),
                    'verified':channel_details.verified,
                    
                }
            view_auth_profile = VideoViews.objects.filter(~Q(Profile=0),video=data['id']).values('Profile').distinct().count()
            view_guest_profile = VideoViews.objects.filter(Profile=0,video=data['id']).values('ip_address').distinct().count()
            data['views']=view_auth_profile+view_guest_profile
            
        return response