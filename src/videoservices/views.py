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
from rest_framework import status
from django.db.models import Count
from videoservices.models import *
from rest_framework import mixins
from custom_decorator import *
from rest_framework.views import APIView
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from threading import Thread  # for threading
import datetime
from urllib import request

# from moviepy.editor import *



class EditProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = EditProfileSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class VerifiedProfileRequestView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = VerifiedProfileRequestViewSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
class ProfileOrChannelDetailsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
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
        try:
            current_user_profile = request.user.profile.id
            print("current_user_profile",current_user_profile)
            response = super(self.__class__,self).get(request, *args, **kwargs)
            response1 = response.data['results'] if 'results' in response.data else response.data
            for data in response1:
                # print("data",data)
                subs_count = Subscription.objects.filter(subscribe=data['id']).\
                                values_list('profile',flat=True).distinct().count()
                country_details = CountryCode.objects.filter(id=data['country_code']).values('name','dial_code','code')
                data['subscriber_counts'] = subs_count if subs_count else 0
                data['country_details'] = country_details[0] if country_details else {}
                subscribed_or_not = Subscription.objects.filter(profile=current_user_profile,subscribe=data['id'],is_deleted=False).exists()
                if subscribed_or_not:
                    data['is_subscribed']=  Subscription.objects.get(profile=current_user_profile,subscribe=data['id'],is_deleted=False).is_subscribed
                else:
                    data['is_subscribed']=False
                channel_details = Profile.objects.get(id=data['id'])
                data['verified_user_status']={'status_value':channel_details.verified,
                                            'status':channel_details.get_verified_display()}
            return response
        except Exception:
            response = super(self.__class__,self).get(request, *args, **kwargs)
            response1 = response.data['results'] if 'results' in response.data else response.data
            for data in response1:
                # print("data",data)
                subs_count = Subscription.objects.filter(subscribe=data['id']).\
                                values_list('profile',flat=True).distinct().count()
                country_details = CountryCode.objects.filter(id=data['country_code']).values('name','dial_code','code')
                data['subscriber_counts'] = subs_count if subs_count else 0
                data['country_details'] = country_details[0] if country_details else {}
                channel_details = Profile.objects.get(id=data['id'])
                data['verified_user_status']={'status_value':channel_details.verified,
                                            'status':channel_details.get_verified_display()}
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

class RemoveProfileImageView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = RemoveProfileImageViewSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class RemoveProfileSubChildImageView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = SubChildProfile.objects.filter(is_deleted=False)
    serializer_class = RemoveProfileSubChildImageViewSerializer

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
            return self.queryset.filter(profile_id=int(profile),is_subscribed=True)
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
                    'image': request.build_absolute_uri(subscribe_details.image.url) if subscribe_details.image else None,
                    'subscribed_count':Subscription.objects.filter(subscribe=subscribe_details.id).\
                        values_list('profile',flat=True).distinct().count(),
                    'verified':subscribe_details.verified,
                    
                }
            else:
                data['subscribe_details']={
                    'id':subscribe_details.id,
                    'user_id':subscribe_details.user_id,
                    'company_name': subscribe_details.company_name,
                    'address': subscribe_details.address,
                    'image': request.build_absolute_uri(subscribe_details.image.url) if subscribe_details.image else None,
                    'subscribed_count':Subscription.objects.filter(subscribe=subscribe_details.id).\
                        values_list('profile',flat=True).distinct().count(),
                    'verified':subscribe_details.verified,
                    
                }

        print("response",response)
        return response

class UnSubscribeChannelAddView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Subscription.objects.filter(is_deleted=False)
    serializer_class = UnSubscribeChannelAddSerializer

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)

class UploadVideoAddView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Video.objects.filter(is_deleted=False)
    serializer_class = UploadVideoAddSerializer
    pagination_class = CSPageNumberPagination

    def get_queryset(self):
        vid_id = self.request.query_params.get('vid_id', None)
        if vid_id:
            return self.queryset.filter(id=vid_id,is_deleted=False)
        else:
            return self.queryset



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
                                update(title=title,description=description,featured_video=featured_video,
                                category=category,private_video=private_video,private_code=private_code,
                                term_and_conditions=term_and_conditions,age_range=age_range,updated_by=updated_by)
        
        previous_tag_list = VideoTags.objects.filter(video_id=vid_id,is_deleted=False).values_list('tags',flat=True)
        print("previous_tag_list",previous_tag_list)
        deleted_tag_list = list(set(previous_tag_list)-set(tags))
        print("deleted_tag_list",deleted_tag_list)
        added_tag_list = list(set(tags)-set(previous_tag_list))
        print("added_tag_list",added_tag_list)
        if deleted_tag_list:
            delete_menu = VideoTags.objects.filter(video_id=vid_id,tags__in=deleted_tag_list).update(is_deleted=True)
        if added_tag_list:
            for tag in added_tag_list:
                VideoTags.objects.create(video_id=vid_id,tags=tag)

        if video_details_update:
            data = Video.objects.get(id=vid_id,is_deleted=False)
            data.__dict__.pop('_state')
            data.__dict__['video']=request.build_absolute_uri(data.video.url)
            data.__dict__['tags']=tags
            return Response({'results': data.__dict__,
                                'msg': 'success',
                                "request_status": 1})
        else:
            return Response({'results': [],
                            'msg': 'fail',
                            "request_status": 0})

class DeleteVideoView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Video.objects.filter(is_deleted=False)
    serializer_class = DeleteVideoSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        return super(self.__class__,self).put(request, *args, **kwargs)

class VideoListView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    queryset = Video.objects.filter(is_deleted=False)
    serializer_class = VideoListViewSerializer

    def post(self, request, *args, **kwargs):
        # tag_name = self.request.query_params.get('tag_name', None)
        vid_id = request.data.get('vid_id')
        action = request.data.get('action') if request.data.get('action') else None
        print("vid_id",vid_id)
        
        # response = super(self.__class__,self).get(request, *args, **kwargs)
        video_details = self.queryset.filter(id=vid_id)
        data_dict = {}
        for data in video_details:
            if action is not None and action.lower() == 'edit':
                data_dict['id']=data.id
                data_dict['channel']=data.channel.id
                data_dict['video']=request.build_absolute_uri(data.video.url)
                data_dict['title']=data.title
                data_dict['description']=data.description
                data_dict['category']={'id':data.category.id,'name':data.category.name}
                data_dict['private_video']=data.private_video
                if data.private_video == True:
                    print("private_video",data.private_video)
                    data_dict['private_code']=data.private_code

                data_dict['featured_video']=data.featured_video
                data_dict['term_and_conditions']=data.term_and_conditions
                data_dict['age_range']=data.age_range
                data_dict['is_deleted']=data.is_deleted
            else:
                data_dict['id']=data.id
                data_dict['channel']=data.channel.id
                data_dict['video']=request.build_absolute_uri(data.video.url)
                data_dict['title']=data.title
                data_dict['description']=data.description
                data_dict['category']={'id':data.category.id,'name':data.category.name}
                data_dict['private_video']=data.private_video
                data_dict['featured_video']=data.featured_video
                data_dict['term_and_conditions']=data.term_and_conditions
                data_dict['age_range']=data.age_range
                data_dict['is_deleted']=data.is_deleted


            
            link_list = []
            thumbnail = VideoThumbnailDocuments.objects.filter(video=data.id,is_deleted=False)
            for link in thumbnail:
                link_list.append(request.build_absolute_uri(link.thumbnail.url))
            
            data_dict['thumbnail_stack']=link_list
            channel_details = Profile.objects.get(id=data.channel.id)
            if request.user.is_authenticated:
                current_user_profile = request.user.profile.id
                print("current_user_profile",current_user_profile)
                subscribed_or_not = Subscription.objects.filter(profile=current_user_profile,subscribe=data.channel.id,is_deleted=False).exists()


                if channel_details.account !='Company':
                    data_dict['channel_details']={
                        'id':channel_details.id,
                        'user_id':channel_details.user_id,
                        'firstname':channel_details.firstname,
                        'lastname': channel_details.lastname,
                        'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                        'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                            values_list('profile',flat=True).distinct().count(),
                        'is_subscribed':  Subscription.objects.get(profile=current_user_profile,
                                        subscribe=data.channel.id,is_deleted=False).is_subscribed if subscribed_or_not
                                        else False,
                        'verified':channel_details.verified,
                        
                        
                    }
                else:
                    data_dict['channel_details']={
                        'id':channel_details.id,
                        'user_id':channel_details.user_id,
                        'company_name': channel_details.company_name,
                        'address': channel_details.address,
                        'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                        'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                            values_list('profile',flat=True).distinct().count(),
                        'is_subscribed':Subscription.objects.get(profile=current_user_profile,
                                        subscribe=data.channel.id,is_deleted=False).is_subscribed if subscribed_or_not
                                        else False,
                        'verified':channel_details.verified,
                        
                        
                    }
            else:
                if channel_details.account !='Company':
                    data_dict['channel_details']={
                        'id':channel_details.id,
                        'user_id':channel_details.user_id,
                        'firstname':channel_details.firstname,
                        'lastname': channel_details.lastname,
                        'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                        'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                            values_list('profile',flat=True).distinct().count(),
                        'is_subscribed':False
                        
                        
                    }
                else:
                    data_dict['channel_details']={
                        'id':channel_details.id,
                        'user_id':channel_details.user_id,
                        'company_name': channel_details.company_name,
                        'address': channel_details.address,
                        'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                        'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                            values_list('profile',flat=True).distinct().count(),
                        'is_subscribed':False
                        
                        
                    }
            view_auth_profile = VideoViews.objects.filter(~Q(Profile=0),video=data.id).values('Profile').distinct().count()
            view_guest_profile = VideoViews.objects.filter(Profile=0,video=data.id).values('ip_address').distinct().count()
            data_dict['views']=view_auth_profile+view_guest_profile
            data_dict['tags']=VideoTags.objects.filter(video=vid_id,is_deleted=False).values_list('tags',flat=True).distinct()
        if len(data_dict)>0:
            return Response({'request_status':1,
                                'results':data_dict,
                                'msg':'success'
                                },
                                status=status.HTTP_200_OK)
        else:
            return Response({'request_status':0,
                                'results':[],
                                'msg':'No Data Found'
                                },
                                status=status.HTTP_200_OK)


class WatchHistoryVideoListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    queryset = VideoViews.objects.filter(is_deleted=False)

    def post(self, request, *args, **kwargs):
        profile_id = request.user.profile.id
        vid_id = self.queryset.filter(Profile=profile_id).values_list('video',flat=True).distinct()
        print("vid_id",list(vid_id))
        watch_history=[]
        video_details = Video.objects.filter(id__in=list(vid_id),is_deleted=False)
        print("video_details",video_details)
        
        for data in video_details:
            data_dict = {}
            print("data",data.channel.id,data.title)
            data_dict['id']=data.id
            data_dict['channel']=data.channel.id
            data_dict['video']=request.build_absolute_uri(data.video.url)
            data_dict['title']=data.title
            data_dict['description']=data.description
            data_dict['category']={'id':data.category.id,'name':data.category.name}
            data_dict['private_video']=data.private_video
            data_dict['featured_video']=data.featured_video
            data_dict['term_and_conditions']=data.term_and_conditions
            data_dict['age_range']=data.age_range
            data_dict['is_deleted']=data.is_deleted
            
            link_list = []
            thumbnail = VideoThumbnailDocuments.objects.filter(video=data.id)
            for link in thumbnail:
                link_list.append(request.build_absolute_uri(link.thumbnail.url))
            
            data_dict['thumbnail_stack']=link_list
            channel_details = Profile.objects.get(id=data.channel.id)

            current_user_profile = request.user.profile.id
            print("current_user_profile",current_user_profile)
            subscribed_or_not = Subscription.objects.filter(profile=current_user_profile,subscribe=data.channel.id,is_deleted=False).exists()


            if channel_details.account !='Company':
                data_dict['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'firstname':channel_details.firstname,
                    'lastname': channel_details.lastname,
                    'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count(),
                    'is_subscribed':  Subscription.objects.get(profile=current_user_profile,
                                    subscribe=data.channel.id,is_deleted=False).is_subscribed if subscribed_or_not
                                    else False,
                    'verified':channel_details.verified,
                    
                    
                }
            else:
                data_dict['channel_details']={
                    'id':channel_details.id,
                    'user_id':channel_details.user_id,
                    'company_name': channel_details.company_name,
                    'address': channel_details.address,
                    'image': request.build_absolute_uri(channel_details.image.url) if channel_details.image else None,
                    'subscribed_count':Subscription.objects.filter(subscribe=channel_details.id).\
                        values_list('profile',flat=True).distinct().count(),
                    'is_subscribed':Subscription.objects.get(profile=current_user_profile,
                                    subscribe=data.channel.id,is_deleted=False).is_subscribed if subscribed_or_not
                                    else False,
                    'verified':channel_details.verified,
                    
                    
                }
            
            view_auth_profile = VideoViews.objects.filter(~Q(Profile=0),video=data.id).values('Profile').distinct().count()
            view_guest_profile = VideoViews.objects.filter(Profile=0,video=data.id).values('ip_address').distinct().count()
            data_dict['views']=view_auth_profile+view_guest_profile
            data_dict['tags']=VideoTags.objects.filter(video=data.id).values_list('tags',flat=True).distinct()
            watch_history.append(data_dict)
        print("watch_history",watch_history)
        if len(watch_history)>0:
            return Response({'request_status':1,
                                'results':watch_history,
                                'msg':'success'
                                },
                                status=status.HTTP_200_OK)
        else:
            return Response({'request_status':0,
                                'results':[],
                                'msg':'No Data Found'
                                },
                                status=status.HTTP_200_OK)


class TagsListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = VideoTags.objects.filter(is_deleted=False)

    def post(self, request, *args, **kwargs):
        # tag_name = self.request.query_params.get('tag_name', None)
        tag_name = request.data.get('tag_name')
        print("tagname",tag_name)
        if tag_name:
            suggestions = VideoTags.objects.filter(tags__icontains=tag_name).values_list('tags',flat=True).distinct()
        elif tag_name == '' or tag_name == None:
            suggestions = VideoTags.objects.values('tags').order_by('tags').\
                annotate(tag_count=Count('tags')).order_by('-tag_count')[:10].values_list('tags',flat=True)
            print("top_suggestions",suggestions)

        else:
            suggestions = VideoTags.objects.values('tags').order_by('tags').\
                annotate(tag_count=Count('tags')).order_by('-tag_count')[:10].values_list('tags',flat=True)
            print("top_suggestions",suggestions)

        if len(suggestions)>0:
            return Response({'request_status':1,
                                'results':{
                                    'tags':list(suggestions),
                                    'msg':'success'
                                    },
                                },
                                status=status.HTTP_200_OK)
        else:
            return Response({'request_status':0,
                                'results':{
                                    'tags':[],
                                    'msg':'No Data Found'
                                    },
                                },
                                status=status.HTTP_200_OK)

        


class UploadVideoThumbnailAddView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = VideoThumbnailDocuments.objects.filter(is_deleted=False)
    serializer_class = UploadVideoThumbnailAddViewSerializer

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            vid_id = self.request.query_params.get('vid_id', None)
            updated_by=request.user
            with transaction.atomic():
                print("thumbnail",request.data)
                
                request.data._mutable =True # Making Querydict Mutable as for requirement Please use with caution 
                old_thumbnail_list=list(request.data.pop('old_thumbnail_list')) if request.data.get('old_thumbnail_list') else []
                # old_thumbnail_list=old_thumbnail_list.split(',')
                print("old_thumbnail_list",old_thumbnail_list,type(old_thumbnail_list))
                from django.conf import settings
                host = settings.SITE_URL
                old_thumbnail_list_wo_domail=[x[len(host):] for x in old_thumbnail_list if host in x]
                print("old_thumbnail_list_wo_domail",old_thumbnail_list_wo_domail)
                previous_image_url = VideoThumbnailDocuments.objects.filter(video=vid_id,is_deleted=False).values_list('thumbnail',flat=True)
                print("previous_image_url",previous_image_url)
                deleted_image_url = list(set(previous_image_url)-set(old_thumbnail_list_wo_domail))
                delete_image = VideoThumbnailDocuments.objects.filter(video=vid_id,thumbnail__in=deleted_image_url).update(is_deleted=True)
                print("sonme test ",request.data.get('thumbnail'))
                list_data_image=list(request.data.pop('thumbnail')) if request.data.get('thumbnail') else []
                print("list_data_image",list_data_image)
                request.data._mutable =False # restoring Querydict imMutable as for requirement Please use with caution
                upload=None
                if list_data_image:
                    for img in list_data_image:
                        upload = VideoThumbnailDocuments.objects.create(video_id=vid_id,thumbnail=img)
                
                if upload or delete_image or old_thumbnail_list:
                    return Response({'results': VideoThumbnailDocuments.objects.filter(video=vid_id,is_deleted=False).values_list('thumbnail',flat=True),
                                        'msg': 'success',
                                        "request_status": 1})
                else:
                    return Response({'results': [],
                                    'msg': 'fail',
                                    "request_status": 0})
        except Exception as e:
            raise e

class VideoListingGenereView(generics.ListAPIView):

    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = Video.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = VideoListingGenereViewAddSerializer
    

    def get_queryset(self):
        category = self.request.query_params.get('category',None)
        if category:
            return self.queryset.filter(category__name__iexact=category)
        else:
            return self.queryset


    @response_modify_decorator_list_or_get_after_execution_for_pagination
    def get(self, request, *args, **kwargs):
        response = super(self.__class__,self).get(request, *args, **kwargs)
        for data in response.data['results']:
            link_list = []
            thumbnail = VideoThumbnailDocuments.objects.filter(video=data['id'],is_deleted=False)
            for link in thumbnail:
                link_list.append(request.build_absolute_uri(link.thumbnail.url))
            data['thumbnail_stack']=link_list
            # "/uploads/media/"
            # clip = (VideoFileClip(data['video'])
            #         .subclip((0,0.1),(0,8))
            #         .resize(0.3))
            # clip.write_gif('uploads/media/thumpgif/'+data['title']+".gif")



            
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


class VideoViewsViewAdd(generics.ListCreateAPIView):

    permission_classes = [AllowAny]
    pagination_class = CSPageNumberPagination
    queryset = VideoViews.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = VideoViewsViewAddSerializer

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)
    

  
class HomeVideoListingView(generics.ListAPIView):

    permission_classes = [AllowAny]
    # authentication_classes = []
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
    # authentication_classes = [TokenAuthentication]
    pagination_class = CSPageNumberPagination
    queryset = Video.objects.filter(is_deleted=False,updated_by__isnull=False,
                title__isnull=False,description__isnull=False).order_by('-id')
    serializer_class = ChannelVideoListingViewSerializer
    

    def get_queryset(self):
        channel_id = self.request.query_params.get('channel_id',None)
        return self.queryset.filter(channel=channel_id)

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

class CountryCodeViewAdd(generics.ListCreateAPIView):

    permission_classes = [AllowAny]
    queryset = CountryCode.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = CountryCodeViewAddSerializer
    filter_backends=(DjangoFilterBackend,)

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)

    
    @response_modify_decorator_get
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)


class GenereAddListView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Genere.objects.filter(is_deleted=False)
    serializer_class = GenereAddListViewSerializer
    pagination_class = OnOffPagination

    def get_queryset(self):
        cat_id = self.request.query_params.get('cat_id', None)
        if cat_id:
            return self.queryset.filter(id=cat_id,is_deleted=False)
        else:
            return self.queryset

    @response_modify_decorator_list_or_get_after_execution_for_onoff_pagination
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        cat_id = self.request.query_params.get('cat_id', None)
        method = self.request.query_params.get('method', None)
        updated_by=request.user
        with transaction.atomic():
            if method.lower() == 'edit':
                name=request.data['name'] if request.data['name'] else None
                icon=request.data['icon'] if request.data['icon'] else None
                url=request.data['url'] if request.data['url'] else None
                genere_update = Genere.objects.filter(id=cat_id,is_deleted=False).\
                                        update(name=name,icon=icon,url=url,
                                        updated_by=updated_by)
                if genere_update:
                    data = Genere.objects.get(id=cat_id,is_deleted=False)
                    data.__dict__.pop('_state')
                    return Response({'results': data.__dict__,
                                        'msg': 'success',
                                        "request_status": 1})
                else:
                    return Response({'results': [],
                                    'msg': 'fail',
                                    "request_status": 0})
            
            elif method.lower() == 'delete':
                genere_update = Genere.objects.filter(id=cat_id,is_deleted=False).\
                                        update(is_deleted=True)
                if genere_update:
                    return Response({'results':{
                                        'cat_id':cat_id ,
                                        },
                                        'msg': 'deleted successfully',
                                        "request_status": 1})
                else:
                    return Response({'results': [],
                                    'msg': 'fail to delete',
                                    "request_status": 0})


class CatagoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    queryset = Genere.objects.filter(is_deleted=False)

    def get(self, request, *args, **kwargs):

        genere_list = Genere.objects.filter().values('id','name','url','icon').distinct()
        if len(genere_list)>0:
            return Response({'request_status':1,
                                'results':{
                                    'geners':list(genere_list),
                                    'msg':'success'
                                    },
                                },
                                status=status.HTTP_200_OK)
        else:
            return Response({'request_status':0,
                                'results':{
                                    'geners':[],
                                    'msg':'No Data Found'
                                    },
                                },
                                status=status.HTTP_200_OK)

class PrivateVideoCheckView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Video.objects.filter(is_deleted=False)

    def post(self, request, format=None):
        try:
            with transaction.atomic():
                vid_id = request.data["vid_id"]
                private_code = request.data["private_code"]
                valid_or_not = self.queryset.filter(id=vid_id,private_code=private_code).exists()
                print("valid_or_not",valid_or_not)
                if valid_or_not == False:
                    return Response({'request_status': 0,
                            'results':{
                                'msg':'code does not match'
                                },
                            },
                            status=status.HTTP_200_OK)
                else:
                    return Response({'request_status': 1,
                            'results':{
                                'msg':'success'
                                },
                            },
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise e