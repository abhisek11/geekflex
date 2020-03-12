from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from django.conf import settings
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from drf_extra_fields.fields import Base64ImageField # for image base 64
from django.db import transaction, IntegrityError
from videoservices.models import *
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from threading import Thread  # for threading
import datetime
from custom_functions import get_client_ip
# from .models import Help
# from .models import Feedback
# from .models import Sponsors
# from .models import Service

class EditProfileSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    image = serializers.FileField(required=False)
    subscribed_count=serializers.IntegerField(required=False)
    company_name = serializers.CharField(required=False)
    class Meta:
        model=Profile
        fields='__all__'

    def update(self, instance, validated_data):
        try:
            '''
            Test--data
            BODY- PARAMETERS(
                    account:Parent
                    image:path___image.png
                    firstname:Abhisek
                    lastname:Singh
                    company_name:XYZ
                    dob:1994-12-19
                    gender:M
                    phone:7595914579
                    )
            '''

            updated_by = validated_data.get('updated_by')
            with transaction.atomic():
                if instance.account != 'Company':
                    # instance.image = validated_data.get('image')
                    instance.firstname = validated_data.get('firstname')
                    instance.lastname = validated_data.get('lastname')
                    instance.company_name = validated_data.get('company_name')
                    instance.dob = validated_data.get('dob')
                    instance.gender = validated_data.get('gender')
                    instance.phone = validated_data.get('phone')
                    instance.country_code=validated_data.get('country_code')
                    instance.dial_code=validated_data.get('dial_code')
                    instance.updated_by = updated_by
                    instance.__dict__['subscribed_count']=Subscription.objects.filter(subscribe=instance.id).\
                        values_list('profile',flat=True).distinct().count()
                    instance.save()
                else:
                    instance.company_name = validated_data.get('company_name')
                    instance.phone = validated_data.get('phone')
                    instance.country_code=validated_data.get('country_code')
                    instance.dial_code=validated_data.get('dial_code')
                    instance.address = validated_data.get('address')
                    instance.updated_by = updated_by
                    instance.__dict__['subscribed_count']=Subscription.objects.filter(subscribe=instance.id).\
                        values_list('profile',flat=True).distinct().count()
                    instance.save()
                return instance
        except Exception as e:
            raise e

class VerifiedProfileRequestViewSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Profile
        fields=('id','verified','updated_by','updated_at','owned_by')
    
class ProfileOrChannelDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    subscriber_counts = serializers.IntegerField(required=False)
    country_details = serializers.DictField(required=False)
    image = serializers.FileField(required=False)
    verified_user_status=serializers.DictField(required=False)

    class Meta:
        model=Profile
        fields='__all__'

class EditProfileImageSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Profile
        fields=('id','image','updated_by','owned_by')
    

class RemoveProfileImageViewSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Profile
        fields=('id','image','updated_by','owned_by')
    
    def update(self,instance, validated_data):
        updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
        try:
            updated_by = validated_data.get('updated_by')
            instance.image=None
            instance.updated_by=updated_by
            instance.save()
            return instance
        except Exception as e:
            raise e

class RemoveProfileSubChildImageViewSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Profile
        fields=('id','image','updated_by','owned_by')
    
    def update(self,instance, validated_data):
        updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
        try:
            updated_by = validated_data.get('updated_by')
            instance.image=None
            instance.updated_by=updated_by
            instance.save()
            return instance
        except Exception as e:
            raise e


class EditSubChildProfileImageViewSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Profile
        fields=('id','image','updated_by','owned_by')
class SubscribeChannelAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    subscribe_details = serializers.DictField(required=False)

    class Meta:
        model=Subscription
        fields=('id','profile','subscribe','is_subscribed','subscribe_details','created_by','owned_by','updated_by')

    def create(self,validated_data):
        try:
            created_by= validated_data.get('created_by')
            owned_by= validated_data.get('owned_by')
            updated_by = validated_data.get('updated_by')
            profile = validated_data.get('profile')
            subscribe= validated_data.get('subscribe')
            with transaction.atomic():
                subscribed_or_not = Subscription.objects.filter(profile=profile,subscribe=subscribe,is_deleted=False).exists()
                if subscribed_or_not:
                    subscribe = Subscription.objects.filter(profile=profile,subscribe=subscribe,is_deleted=False).\
                        update(is_subscribed=True,updated_by=updated_by)
                else:
                    subscribe = Subscription.objects.create(profile=profile,subscribe=subscribe,
                                is_subscribed=True,created_by=created_by,owned_by=owned_by)
                
                validated_data['is_subscribed'] =  True
                return validated_data

        except Exception as e:
            raise e

    
class UnSubscribeChannelAddSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Subscription
        fields=('id','profile','subscribe','is_subscribed','updated_by','updated_at')
    
    def create(self,validated_data):
        try:
            profile = validated_data.get('profile')
            subscribe= validated_data.get('subscribe')
            updated_by = validated_data.get('updated_by')
            with transaction.atomic():
                unsubscribe = Subscription.objects.filter(profile=profile,
                    subscribe=subscribe,is_deleted=False).\
                    update(is_subscribed=False,updated_by=updated_by)
                return validated_data

        except Exception as e:
            raise e



class UploadVideoAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    tags =  serializers.ListField(required=False)
    class Meta:
        model=Video
        fields=('__all__')

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            video_data = validated_data.get('video')
            channel= validated_data.get('channel')
            # genere = validated_data.get('genere')
            with transaction.atomic():
                # upload = Video.objects.create(video=video_data,profile=profile,genere=genere)
                upload = Video.objects.create(video=video_data,channel=channel)
               
                # validated_data['video'] =  request.build_absolute_uri(upload.video.url)
                validated_data['video'] =  upload.video
                validated_data['id']=upload.id
                return validated_data

        except Exception as e:
            raise e

class DeleteVideoSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Video
        fields=('id','is_deleted','updated_by','title','owned_by')
class VideoListViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    action =  serializers.CharField(required=False)
    class Meta:
        model=Video
        exclude=('private_code',)

class TagsListViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # tags =  serializers.ListField(required=False)
    class Meta:
        model=VideoTags
        fields=('__all__')

class UploadVideoThumbnailAddViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    old_thumbnail_list = serializers.ListField(required=False)
    thumbnail = serializers.FileField(required=False)
    class Meta:
        model=VideoThumbnailDocuments
        fields='__all__'
        
class VideoListingGenereViewAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    private_code =  serializers.CharField(required=False)
    class Meta:
        model=Video
        fields='__all__'

class VideoViewsViewAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    ip_address= serializers.IPAddressField(required=False)
    class Meta:
        model=VideoViews
        fields='__all__'

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            print("request.user.is_authenticated",request.user.is_authenticated)
            if request.user.is_authenticated:
                profile_id = request.user.profile.id
                created_by = validated_data.get('created_by')
            else:
                profile_id=0
                created_by = None
            video= validated_data.get('video')
            
            ip_address = get_client_ip(request)
            # ip = ip_address(request)
            with transaction.atomic():
                exist_or_not = VideoViews.objects.filter(Profile=profile_id,video=video,is_deleted=False)
                if not exist_or_not:
                    video_view = VideoViews.objects.create(Profile=profile_id,video=video,
                                                            ip_address=ip_address,created_by=created_by)
                    validated_data['id']=video_view.id
                    # validated_data['video'] =  request.build_absolute_uri(upload.video.url)
                validated_data['profile_id'] =  profile_id
                validated_data['ip_address'] =  ip_address
                
                return validated_data

        except Exception as e:
            raise e

class CountryCodeViewAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    country_codes = serializers.ListField(required=False)
    class Meta:
        model=CountryCode
        fields='__all__'

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            with transaction.atomic():
                for extention_data in validated_data.get("country_codes"):
                    country_code_create = CountryCode.objects.create(**extention_data)
                return validated_data

        except Exception as e:
            raise e


class HomeVideoListingViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    private_code =  serializers.CharField(required=False)
    class Meta:
        model=Video
        fields='__all__'


class SubChildUserDetailsViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    image= serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    profile = serializers.CharField(required=False)
    class Meta:
        model=Profile
        fields=('__all__')
class ChannelVideoListingViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # private_code =  serializers.CharField(required=False)
    class Meta:
        model=Video
        # fields=('__all__')
        exclude=('private_code',)


class GenereAddListViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    genere_data=serializers.ListField(required=False)
    name = serializers.CharField(required=False)
    class Meta:
        model=Genere
        fields=('__all__')

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            genere_data = validated_data.get('genere_data')
            created_by=validated_data.get('created_by')
            owned_by=validated_data.get('owned_by')

            with transaction.atomic():
                for g_data in genere_data:
                    genere_add = Genere.objects.create(**g_data,created_by=created_by,
                                                        owned_by=owned_by)

                return validated_data

        except Exception as e:
            raise e

class HelpSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Help
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Feedback
        fields = '__all__'

class SponsorsSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Sponsors
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Service
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Career
        fields = '__all__'

class AboutSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = About
        fields = '__all__'

class TermsConditionsViewSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = TermsConditions
        fields = '__all__'

class PrivacyPolicyViewSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class WatchTimerLogSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model = WatchTimerLog
        fields = '__all__'