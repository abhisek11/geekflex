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

class SignupAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Profile
        fields='__all__'

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            video_data = validated_data.get('video')
            channel= validated_data.get('channel')
            channel= validated_data.get('channel')
            channel= validated_data.get('channel')
            channel= validated_data.get('channel')
            channel= validated_data.get('channel')
            channel= validated_data.get('channel')
            channel= validated_data.get('channel')
            with transaction.atomic():


                return validated_data

        except Exception as e:
            raise e
