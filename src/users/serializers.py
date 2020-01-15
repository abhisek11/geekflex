from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import *
from rest_framework.exceptions import APIException
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings
from custom_exception_message import *
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from drf_extra_fields.fields import Base64ImageField # for image base 64
from django.db import transaction, IntegrityError
from videoservices.models import *
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from threading import Thread  # for threading
import datetime
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

class SignupAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    user = serializers.DictField(required=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model=Profile
        fields='__all__'

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            account = validated_data.get('account') if validated_data.get('account') else 'Individual'
            image= validated_data.get('image') if validated_data.get('image') else None
            firstname= validated_data.get('firstname') if validated_data.get('firstname') else None
            lastname= validated_data.get('lastname') if validated_data.get('lastname') else None
            company_name = validated_data.get('company_name') if validated_data.get('company_name') else None
            email= validated_data.get('email') if validated_data.get('email') else None
            dob= validated_data.get('dob') if validated_data.get('dob') else None
            gender= validated_data.get('gender') if validated_data.get('gender') else None
            phone= validated_data.get('phone') if validated_data.get('phone') else None
            password = validated_data.get('password') if validated_data.get('password') else None
            confirm_password = validated_data.get('confirm_password') if validated_data.get('confirm_password') else None
            with transaction.atomic():
                if email is None or password is None:
                    custom_exception_message(self,None,"Please provide both email and password ")
                else:
                    if password == confirm_password:
                        print("pasword matched ")
                        # pwd = make_password(password)
                        if User.objects.filter(email = email).exists():
                            print("test user")
                            custom_exception_message(self,None,"Email ID already taken ")
                        else:
                            user= User.objects.create_user(username = email,email=email,
                                                                    first_name=firstname,last_name=lastname)
                            user.set_password(password)
                            user.is_staff = True #for testing of user 
                            user.save()
                            if account == 'Parent':
                                profile_create,created = Profile.objects.get_or_create(user=user,
                                                                account=account,image=image,firstname=firstname,
                                                                lastname=lastname,company_name=company_name,email=email,
                                                                dob=dob,gender=gender,phone=phone,child_count=2)
                            else:
                                profile_create,created = Profile.objects.get_or_create(user=user,
                                                                account=account,image=image,firstname=firstname,
                                                                lastname=lastname,company_name=company_name,email=email,
                                                                dob=dob,gender=gender,phone=phone)

                            # print("user",user.__dict__)
                    else:
                        custom_exception_message(self,None,"Password did not matched")
                validated_data['image'] = profile_create.image
                validated_data['user']={
                    'user_id':user.__dict__['id'],
                    'user_email':user.__dict__['email']
                }

                return validated_data

        except Exception as e:
            raise e

class LoginSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # user = serializers.DictField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'})
    class Meta:
        model=Profile
        fields='__all__'

    # def create(self,validated_data):
    #     try:
    #         data = {}
    #         username = validated_data.pop('username')
    #         password = validated_data.pop('password')
    #         with transaction.atomic():
    #             if username is None or password is None:
    #                 custom_exception_message(self,None,"Please provide both username and password")
    #             user = authenticate(username=username, password=password)
    #             print("user",user)
    #             if not user:
    #                 custom_exception_message(self,None,'Invalid Credentials')
    #             token, _ = Token.objects.get_or_create(user=user)
    #             data['token'] = token.key
    #             data['username'] = username
    #             data['password'] = password

    #             return Response(data)
    #     except Exception as e:
    #         raise e