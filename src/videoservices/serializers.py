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

class EditProfileSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    image = serializers.FileField(required=False)
    subscribed_count=serializers.IntegerField(required=False)
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
                    instance.updated_by = updated_by
                    instance.__dict__['subscribed_count']=Subscription.objects.filter(subscribe=instance.id).\
                        values_list('profile',flat=True).distinct().count()
                    instance.save()
                else:
                    instance.company_name = validated_data.get('company_name')
                    instance.phone = validated_data.get('phone')
                    instance.address = validated_data.get('address')
                    instance.updated_by = updated_by
                    instance.__dict__['subscribed_count']=Subscription.objects.filter(subscribe=instance.id).\
                        values_list('profile',flat=True).distinct().count()
                    instance.save()
                return instance
        except Exception as e:
            raise e
class ProfileOrChannelDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    subscriber_counts = serializers.IntegerField(required=False)
    image = serializers.FileField(required=False)

    class Meta:
        model=Profile
        fields='__all__'

class EditProfileImageSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model=Profile
        fields=('id','image','updated_by','owned_by')

class EditSubChildProfileImageViewSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model=SubChildProfile
        fields=('id','image','updated_by','owned_by')
class SubscribeChannelAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    subscribe_details = serializers.DictField(required=False)

    class Meta:
        model=Subscription
        fields=('__all__')

    def create(self,validated_data):
        try:
            profile = validated_data.get('profile')
            subscribe= validated_data.get('subscribe')
            with transaction.atomic():
                subscribe = Subscription.objects.create(profile=profile,subscribe=subscribe,is_subscribed=True)
                validated_data['is_subscribed'] =  subscribe.is_subscribed
                validated_data['id']=subscribe.id
                return validated_data

        except Exception as e:
            raise e

    

class UploadVideoAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # private_code =  serializers.CharField(required=False)
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


class UploadVideoThumpnailAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=VideoThumpnilDocuments
        fields='__all__'
        
class VideoListingGenereViewAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    private_code =  serializers.CharField(required=False)
    class Meta:
        model=Video
        fields='__all__'

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
        model=SubChildProfile
        fields=('id','profile','firstname','lastname','dob','gender','created_by','owned_by','image')
class ChannelVideoListingViewSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    private_code =  serializers.CharField(required=False)
    class Meta:
        model=Video
        fields='__all__'

