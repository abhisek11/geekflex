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

class UploadVideoAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Video
        fields='__all__'

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
                return validated_data

        except Exception as e:
            raise e
