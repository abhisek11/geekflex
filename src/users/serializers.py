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
from django.db.models import Value
from threading import Thread  # for threading
import datetime
from users import views
# from django.core.urlresolvers import reverse_lazy
from mailapp.views import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

class SignupAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    user = serializers.DictField(required=False)
    # image = serializers.FileField(required=False)
    company_name = serializers.CharField(required=False)
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
    photoUrl = serializers.CharField(required=False)
    image = serializers.FileField(required=False)
    class Meta:
        model=Profile
        fields='__all__'

    def create(self,validated_data):
        try:
            request =  self.context.get('request')
            auth_provider = validated_data.get('auth_provider') if validated_data.get('auth_provider') else 'Kidsclub'

            with transaction.atomic():
                if auth_provider == 'Kidsclub':
                    account = validated_data.get('account') if validated_data.get('account') else 'Individual'
                    image= validated_data.get('image') 
                    firstname= validated_data.get('firstname') if validated_data.get('firstname') else ""
                    lastname= validated_data.get('lastname') if validated_data.get('lastname') else ""
                    company_name = validated_data.get('company_name') if validated_data.get('company_name') else None
                    address = validated_data.get('address') if validated_data.get('address') else None
                    email= validated_data.get('email') if validated_data.get('email') else None
                    dob= validated_data.get('dob') if validated_data.get('dob') else None
                    gender= validated_data.get('gender') if validated_data.get('gender') else None
                    phone= validated_data.get('phone') if validated_data.get('phone') else None
                    password = validated_data.get('password') if validated_data.get('password') else None
                    confirm_password = validated_data.get('confirm_password') if validated_data.get('confirm_password') else None
                    is_phone_verified = validated_data.get('is_phone_verified') if validated_data.get('is_phone_verified') else False
                    if email is None or password is None:
                        custom_exception_message(self,None,"Please provide both email and password ")
                    else:
                        if password == confirm_password:
                            print("pasword matched ")
                            # pwd = make_password(password)
                            if User.objects.filter(email = email).exists():
                                print("test user")
                                raise CustomAPIException(None,"Email ID already exist ",status_code=status.HTTP_409_CONFLICT)
                            elif Profile.objects.filter(phone = phone).exists():
                                print("test user")
                                raise CustomAPIException(None,"Phone Number already exist ",status_code=status.HTTP_409_CONFLICT) 
                            else:
                                user= User.objects.create_user(username = email,email=email,
                                                                        first_name=firstname,last_name=lastname)
                                user.set_password(password)
                                # user.is_staff = True #for testing of user 
                                user.is_active = False
                                user.save()
                                current_site = get_current_site(request)
                                # ============= Mail Send ==============#
                                
                                #EMAIL VERIFICATION PART 
                                if company_name:
                                    mail_id = user.email
                                    if mail_id:
                                        mail_data = {
                                            'name': company_name,
                                            'domain': current_site.domain,
                                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                        }
                                        mail_class = GlobleMailSend('UEV', [mail_id])
                                        mail_thread = Thread(target = mail_class.mailsend, args = (mail_data,))
                                        mail_thread.start()

                                else:
                                    mail_id = user.email
                                    if mail_id:
                                        mail_data = {
                                            'name':user.first_name +" "+ user.last_name,
                                            'domain': current_site.domain,
                                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                        }
                                        mail_class = GlobleMailSend('UEV', [mail_id])
                                        mail_thread = Thread(target = mail_class.mailsend, args = (mail_data,))
                                        mail_thread.start()
                                
                                if account == 'Parent':
                                    if image is not None and image is not "":
                                        profile_create,created = Profile.objects.get_or_create(user=user,
                                                                        account=account,image=image,firstname=firstname,
                                                                        lastname=lastname,company_name=company_name,email=email,
                                                                        dob=dob,gender=gender,phone=phone,child_count=2,is_phone_verified=is_phone_verified)

                                    else:    
                                        profile_create,created = Profile.objects.get_or_create(user=user,
                                                                        account=account,firstname=firstname,
                                                                        lastname=lastname,company_name=company_name,email=email,
                                                                        dob=dob,gender=gender,phone=phone,child_count=2,is_phone_verified=is_phone_verified)
                                elif account == 'Company':
                                    if image is not None and image is not "":
                                        profile_create,created = Profile.objects.get_or_create(user=user,
                                                                        account=account,image=image,company_name=company_name,email=email,
                                                                        phone=phone,is_phone_verified=is_phone_verified,address=address)
                                    else:
                                        profile_create,created = Profile.objects.get_or_create(user=user,
                                                                        account=account,company_name=company_name,email=email,
                                                                        phone=phone,is_phone_verified=is_phone_verified,address=address)
                                else:
                                    if image is not None and image is not "":
                                        profile_create,created = Profile.objects.get_or_create(user=user,
                                                                        account=account,image=image,firstname=firstname,
                                                                        lastname=lastname,company_name=company_name,email=email,
                                                                        dob=dob,gender=gender,phone=phone,is_phone_verified=is_phone_verified)
                                    else:
                                        profile_create,created = Profile.objects.get_or_create(user=user,
                                                                        account=account,firstname=firstname,
                                                                        lastname=lastname,company_name=company_name,email=email,
                                                                        dob=dob,gender=gender,phone=phone,is_phone_verified=is_phone_verified)
                                
                                # print("user",user.__dict__)
                        else:
                            custom_exception_message(self,None,"Password did not matched")

                elif auth_provider == 'Facebook' or auth_provider == 'Google':
                    account = validated_data.get('account') if validated_data.get('account') else 'Individual'
                    photoUrl= validated_data.get('photoUrl') 
                    firstname= validated_data.get('firstname') if validated_data.get('firstname') else ""
                    lastname= validated_data.get('lastname') if validated_data.get('lastname') else ""
                    company_name = validated_data.get('company_name') if validated_data.get('company_name') else None
                    address = validated_data.get('address') if validated_data.get('address') else None
                    email= validated_data.get('email') if validated_data.get('email') else None
                    dob= validated_data.get('dob') if validated_data.get('dob') else None
                    gender= validated_data.get('gender') if validated_data.get('gender') else None
                    phone= validated_data.get('phone') if validated_data.get('phone') else None
                    password = ""
                    is_phone_verified = validated_data.get('is_phone_verified') if validated_data.get('is_phone_verified') else False
                    if email is None:
                        custom_exception_message(self,None,"Please provide both email and password ")
                    else:
                        if User.objects.filter(email = email).exists():
                            print("test user")
                            raise CustomAPIException(None,"Email ID already exist ",status_code=status.HTTP_409_CONFLICT)
                        elif Profile.objects.filter(phone = phone).exists():
                            print("test user")
                            raise CustomAPIException(None,"Phone Number already exist ",status_code=status.HTTP_409_CONFLICT) 
                        else:
                            user= User.objects.create_user(username = email,email=email,
                                                                    first_name=firstname,last_name=lastname)
                            user.set_password(password)
                            # user.is_staff = True #for testing of user 
                            user.is_active = True
                            user.save()
                            current_site = get_current_site(request)
                            
                            if account == 'Parent':
                                if photoUrl is not None and photoUrl is not "":
                                    profile_create,created = Profile.objects.get_or_create(user=user,auth_provider=auth_provider,
                                                                    account=account,photoUrl=photoUrl,firstname=firstname,
                                                                    lastname=lastname,company_name=company_name,email=email,
                                                                    dob=dob,gender=gender,phone=phone,child_count=2,is_phone_verified=is_phone_verified)

                                else:    
                                    profile_create,created = Profile.objects.get_or_create(user=user,auth_provider=auth_provider,
                                                                    account=account,firstname=firstname,
                                                                    lastname=lastname,company_name=company_name,email=email,
                                                                    dob=dob,gender=gender,phone=phone,child_count=2,is_phone_verified=is_phone_verified)
                            # elif account == 'Company':
                            #     if image is not None and image is not "":
                            #         profile_create,created = Profile.objects.get_or_create(user=user,
                            #                                         account=account,image=image,company_name=company_name,email=email,
                            #                                         phone=phone,is_phone_verified=is_phone_verified,address=address)
                            #     else:
                            #         profile_create,created = Profile.objects.get_or_create(user=user,
                            #                                         account=account,company_name=company_name,email=email,
                            #                                         phone=phone,is_phone_verified=is_phone_verified,address=address)
                            else:
                                if photoUrl is not None and photoUrl is not "":
                                    profile_create,created = Profile.objects.get_or_create(user=user,auth_provider=auth_provider,
                                                                    account=account,photoUrl=photoUrl,firstname=firstname,
                                                                    lastname=lastname,company_name=company_name,email=email,
                                                                    dob=dob,gender=gender,phone=phone,is_phone_verified=is_phone_verified)
                                else:
                                    profile_create,created = Profile.objects.get_or_create(user=user,auth_provider=auth_provider,
                                                                    account=account,firstname=firstname,
                                                                    lastname=lastname,company_name=company_name,email=email,
                                                                    dob=dob,gender=gender,phone=phone,is_phone_verified=is_phone_verified)

                            # request = {'username':email,'auth_provider':auth_provider}
                            # user = authenticate(request=self.context.get('request'),
                            #         username=email,auth_provider=auth_provider)
                            # login_data = login(request, user)
                            # print("login_data",login_data)
                            # # response = super(LoginView, self).post(request, format=None)
                            # print("user",user)
                validated_data['image'] = profile_create.image
                validated_data['user']={
                    'user_id':user.__dict__['id'],
                    'user_email':user.__dict__['email']
                }

                return validated_data

        except Exception as e:
            raise e

class SignupSubChildUserAddSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    image= serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    profile = serializers.CharField(required=False)
    class Meta:
        model=SubChildProfile
        fields=('id','profile','firstname','lastname','dob','gender','created_by','owned_by','image')

    def create(self,validated_data):
        try:
            owned_by = validated_data.get('owned_by')
            created_by = validated_data.get('created_by')
            data = {}
            request =  self.context['request']
            acc_type = request.user.profile.account
            profile = request.user.profile.id
            print("acc_type",acc_type,profile)
            image= validated_data.get('image') if validated_data.get('image') else ""
            firstname= validated_data.get('firstname') if validated_data.get('firstname') else ""
            lastname= validated_data.get('lastname') if validated_data.get('lastname') else ""
            dob= validated_data.get('dob') if validated_data.get('dob') else None
            gender= validated_data.get('gender') if validated_data.get('gender') else None
            with transaction.atomic():
                if acc_type == 'Parent':
                    sub_child = SubChildProfile.objects.create(profile_id=int(profile),firstname=firstname,
                                                    image=image,lastname=lastname,dob=dob,gender=gender,owned_by=owned_by,created_by=created_by)
                    if sub_child:
                        print('sub_child',sub_child)
                        sub_child.__dict__['profile'] = sub_child.profile
                        sub_child.__dict__['image_url'] = request.build_absolute_uri(sub_child.image.url)
                        return sub_child.__dict__
                else:
                    raise CustomAPIException(None,'Get parent account to use this feature!',status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        except Exception as e:
            raise e 

class EditSubChildProfileViewSerializer(serializers.ModelSerializer):
    updated_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    # image = serializers.FileField(required=False)
    # profile=serializers.IntegerField(required=False)
    class Meta:
        model=SubChildProfile
        fields=('firstname','lastname','dob','gender','updated_by','owned_by')

class AuthCheckerSerializer(serializers.Serializer):
    class Meta:
        model=User
        fields='__all__'

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model=User
        fields='__all__'

class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for password forgot.
    """
    phone_no=serializers.CharField(required=True)
    new_password=serializers.CharField(required=True)
    confirm_password=serializers.CharField(required=True)
    created_by = serializers.CharField(default=serializers.CurrentUserDefault())
    owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
    class Meta:
        model=User
        fields='__all__'












# class LoginSerializer(serializers.ModelSerializer):
#     created_by = serializers.CharField(default=serializers.CurrentUserDefault())
#     owned_by = serializers.CharField(default=serializers.CurrentUserDefault())
#     # user = serializers.DictField(required=False)
#     username = serializers.CharField(required=False)
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         help_text='Leave empty if no change needed',
#         style={'input_type': 'password', 'placeholder': 'Password'})
#     class Meta:
#         model=Profile
#         fields='__all__'

