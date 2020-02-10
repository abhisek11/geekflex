from django.shortcuts import render
from rest_framework import generics
from videoservices.serializers import *
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
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
# from rest_framework.decorators import detail_route

class EditProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = EditProfileSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class ProfileOrChannelDetailsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = ProfileOrChannelDetailsSerializer
    pagination_class = OnOffPagination


    def get_queryset(self):
        channel_id = self.request.query_params.get('channel_id',None)
        if channel_id is not None:
            return self.queryset.filter(id=int(channel_id))
        else:
            return self.queryset

    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        response1 = response.data['results'] if 'results' in response.data else response.data
        for data in response1:
            # print("data",data)
            subs_count = Subscription.objects.filter(subscribe=data['id']).\
                            values_list('profile',flat=True).distinct().count()

            data['subscriber_counts'] = subs_count if subs_count else 0
            # print("subscriber_counts",subs_count)
        return response

class SubChildUserDetailsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]
    queryset = SubChildProfile.objects.filter(is_deleted=False)
    serializer_class = SubChildUserDetailsViewSerializer

    def get_queryset(self):
        subchild_id = self.request.query_params.get('subchild_id',None)
        return self.queryset.filter(id=subchild_id)


    @response_modify_decorator_get_after_execution
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)


class EditProfileImageView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = EditProfileImageSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class EditSubChildProfileImageView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = SubChildProfile.objects.filter(is_deleted=False)
    serializer_class = EditSubChildProfileImageViewSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class SubscribeChannelAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Subscription.objects.filter(is_deleted=False)
    serializer_class = SubscribeChannelAddSerializer
    pagination_class = CSPageNumberPagination

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    
    def get_queryset(self):
        profile = self.request.query_params.get('profile',None)
        if profile is not None:
            return self.queryset.filter(profile_id=int(profile))
        else:
            return self.queryset

    @response_modify_decorator_list_or_get_after_execution_for_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        for data in response.data['results']:
            print("subscribe",data['subscribe'])
            subscribe_details = Profile.objects.get(id=data['subscribe'])

            if subscribe_details.account !='Company':
                data['subscribe_details']={
                    'id':subscribe_details.id,
                    'user_id':subscribe_details.user_id,
                    'firstname':subscribe_details.firstname,
                    'lastname': subscribe_details.lastname,
                    'image': request.build_absolute_uri(subscribe_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=subscribe_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            else:
                data['subscribe_details']={
                    'id':subscribe_details.id,
                    'user_id':subscribe_details.user_id,
                    'company_name': subscribe_details.company_name,
                    'address': subscribe_details.address,
                    'image': request.build_absolute_uri(subscribe_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=subscribe_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }

        print("response",response)
        return response

class UploadVideoAddView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Video.objects.filter(is_deleted=False)
    serializer_class = UploadVideoAddSerializer
    pagination_class = CSPageNumberPagination

    @response_modify_decorator_list_or_get_after_execution_for_pagination
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        vid_id = self.request.query_params.get('vid_id', None)
        updated_by=request.user
        title=request.data['title'] if request.data['title'] else None
        tags=request.data['tags']  if request.data['tags'] else None
        description=request.data['description']  if request.data['description'] else None
        category=request.data['category']  if request.data['category'] else None
        private_video=request.data['private_video']  if request.data['private_video'] else False
        print("private_video",private_video)
        if request.data['private_video'] == '1':
            private_code=request.data['private_code']
        else: 
            private_code=None
        featured_video = request.data['featured_video']
        
        term_and_conditions=request.data['term_and_conditions']  if request.data['term_and_conditions'] else False
        age_range=request.data['age_range']  if request.data['age_range'] else '21+ or above'

        print("private_code",private_code)
        video_details_update = Video.objects.filter(id=vid_id,is_deleted=False).\
                                update(title=title,tags=tags,description=description,featured_video=featured_video,
                                category=category,private_video=private_video,private_code=private_code,
                                term_and_conditions=term_and_conditions,age_range=age_range,updated_by=updated_by)
        if video_details_update:
            data = Video.objects.get(id=vid_id,is_deleted=False)
            data.__dict__.pop('_state')
            data.__dict__['video']=request.build_absolute_uri(data.video.url)
            return Response({'results': data.__dict__,
                                'msg': 'success',
                                "request_status": 1})
        else:
            return Response({'results': [],
                            'msg': 'fail',
                            "request_status": 0})

class UploadVideoThumpnailAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = VideoThumpnilDocuments.objects.filter(is_deleted=False)
    serializer_class = UploadVideoThumpnailAddSerializer
class VideoListingGenereView(generics.ListAPIView):

    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = Video.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = VideoListingGenereViewAddSerializer
    

    def get_queryset(self):
        category = self.request.query_params.get('category',None)
        return self.queryset.filter(category__name__iexact=category)

    @response_modify_decorator_list_or_get_after_execution_for_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        for data in response.data['results']:
            link_list = []
            thumpnail = VideoThumpnilDocuments.objects.filter(video=data['id'])
            for link in thumpnail:
                link_list.append(request.build_absolute_uri(link.thumpnail.url))
            data['thumpnail_stack']=link_list
            channel_details = Profile.objects.get(id=data['channel'])

            if channel_details.account !='Company':
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'firstname':channel_details.firstname,
                    'lastname': channel_details.lastname,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            else:
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'company_name': channel_details.company_name,
                    'address': channel_details.address,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            view_auth_profile = VideoViews.objects.filter(~Q(Profile=0),video=data['id']).values('Profile').distinct().count()
            view_guest_profile = VideoViews.objects.filter(Profile=0,video=data['id']).values('ip_address').distinct().count()
            data['views']=view_auth_profile+view_guest_profile
        return response

class HomeVideoListingView(generics.ListAPIView):

    permission_classes = [AllowAny]
    authentication_classes = []
    pagination_class = OnOffPagination
    queryset = Video.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = HomeVideoListingViewSerializer
    
    def get_queryset(self):
        tab = self.request.query_params.get('tab',None)
        if tab and tab.lower() == 'latest':
            return self.queryset.order_by('-created_at')
        elif tab and tab.lower() == 'recommended':
            return self.queryset.order_by('?')
        elif tab and tab.lower() == 'featured':
            return self.queryset.filter(featured_video=True).order_by('-id')
        else:
            return self.queryset


    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        for data in response.data['results']:
            link_list = []
            thumpnail = VideoThumpnilDocuments.objects.filter(video=data['id'])
            for link in thumpnail:
                link_list.append(request.build_absolute_uri(link.thumpnail.url))
            data['thumpnail_stack']=link_list
            channel_details = Profile.objects.get(id=data['channel'])

            if channel_details.account !='Company':
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'firstname':channel_details.firstname,
                    'lastname': channel_details.lastname,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            else:
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'company_name': channel_details.company_name,
                    'address': channel_details.address,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            view_auth_profile = VideoViews.objects.filter(~Q(Profile=0),video=data['id']).values('Profile').distinct().count()
            view_guest_profile = VideoViews.objects.filter(Profile=0,video=data['id']).values('ip_address').distinct().count()
            data['views']=view_auth_profile+view_guest_profile
        return response 

class HomeVideoListingAuthView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = OnOffPagination
    queryset = Video.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = HomeVideoListingViewSerializer
    
    def get_queryset(self):
        tab = self.request.query_params.get('tab',None)
        if tab and tab.lower() == 'latest':
            return self.queryset.order_by('-created_at')
        elif tab and tab.lower() == 'recommended':
            return self.queryset.order_by('?')
        elif tab and tab.lower() == 'featured':
            return self.queryset.filter(featured_video=True).order_by('-id')
        else:
            return self.queryset


    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        for data in response.data['results']:
            link_list = []
            thumpnail = VideoThumpnilDocuments.objects.filter(video=data['id'])
            for link in thumpnail:
                link_list.append(request.build_absolute_uri(link.thumpnail.url))
            data['thumpnail_stack']=link_list
            channel_details = Profile.objects.get(id=data['channel'])

            if channel_details.account !='Company':
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'firstname':channel_details.firstname,
                    'lastname': channel_details.lastname,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            else:
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'company_name': channel_details.company_name,
                    'address': channel_details.address,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            view_auth_profile = VideoViews.objects.filter(~Q(Profile=0),video=data['id']).values('Profile').distinct().count()
            view_guest_profile = VideoViews.objects.filter(Profile=0,video=data['id']).values('ip_address').distinct().count()
            data['views']=view_auth_profile+view_guest_profile
        return response 


class ChannelVideoListingView(generics.ListAPIView):

    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = Video.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ChannelVideoListingViewSerializer
    

    def get_queryset(self):
        channel_id = self.request.query_params.get('channel_id',None)
        return self.queryset.filter(channel=channel_id)

    @response_modify_decorator_list_or_get_after_execution_for_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        for data in response.data['results']:
            link_list = []
            thumpnail = VideoThumpnilDocuments.objects.filter(video=data['id'])
            for link in thumpnail:
                link_list.append(request.build_absolute_uri(link.thumpnail.url))
            
            data['thumpnail_stack']=link_list
            images=[]


            path = '/uploads/media/thumpgif/' # on Mac: right click on a folder, hold down option, and click "copy as pathname"
            print("path ",'/uploads/media/thumpgif/'+data['title']+'.gif')
            images.save('/uploads/media/thumpgif/'+data['title']+'.gif',
               save_all=True, append_images=data['thumpnail_stack'], optimize=False, duration=40, loop=0)
                        
            print("images",images)
            channel_details = Profile.objects.get(id=data['channel'])

            if channel_details.account !='Company':
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'firstname':channel_details.firstname,
                    'lastname': channel_details.lastname,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            else:
                data['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'company_name': channel_details.company_name,
                    'address': channel_details.address,
                    'image': request.build_absolute_uri(channel_details.image.url),
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count()
                    
                }
            view_auth_profile = VideoViews.objects.filter(~Q(Profile=0),video=data['id']).values('Profile').distinct().count()
            view_guest_profile = VideoViews.objects.filter(Profile=0,video=data['id']).values('ip_address').distinct().count()
            data['views']=view_auth_profile+view_guest_profile
            
        return response
