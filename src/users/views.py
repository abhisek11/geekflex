from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Permission
from rest_framework import status
from knox.models import AuthToken
from knox.settings import CONSTANTS, knox_settings
from rest_framework.exceptions import ValidationError
from custom_exception_message import *
from rest_framework.response import Response
from knox.views import LogoutAllView
from rest_framework import generics
from videoservices.serializers import *
from django.http import JsonResponse
from users.serializers import *
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.http import HttpResponse  
from knox.auth import TokenAuthentication
# from knox.auth.TokenAuthentication import *
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from pagination import CSLimitOffestpagination, CSPageNumberPagination,OnOffPagination
from django_filters.rest_framework import DjangoFilterBackend
import collections
from adminpanel.models import *
from videoservices.models import *
from rest_framework import mixins
from custom_decorator import *
from rest_framework.views import APIView
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from threading import Thread  # for threading
import datetime
from smsapp.views import *
from django.contrib.auth import login
from AuthTokenSerializer import *
from knox_views.views import LoginView as KnoxLoginView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from OTPvarify import TOTPVerification
from kidsclub.settings import REDIRECT_URL as redirect_url
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
def activate(request, uidb64):  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None:  
        user.is_active = True  
        Profile.objects.filter(user=user).update(is_email_verified =True)
        user.save() 
        return redirect(redirect_url+'email-verified/','Thank you for your email confirmation. Now you can login your account.') 
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return redirect(redirect_url+'email-not-verified/','Activation link is invalid!') 
        # return HttpResponse('Activation link is invalid!')

    
class phoneexists(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)

    # @response_modify_decorator_post
    def post(self, request, format=None):
        try:
            with transaction.atomic():
                Phone_number = request.data["phone_no"]
                dial_code = request.data["dial_code"]
                print("Phone_number",Phone_number,type(Phone_number))
                is_exist_number = Profile.objects.filter(phone__iexact=Phone_number,dial_code=dial_code).exists()
                print("is_exist_number",is_exist_number)
                if is_exist_number == True:
                    return Response({'request_status': 0,
                            'results':{
                                'msg':'Sorry!,mobile number already exists,try with another mobile number'
                                },
                            },
                            status=419)
                else:
                    return Response({'request_status': 1,
                            'results':{
                                'msg':'success'
                                },
                            },
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise e

class EmailexistsProfileEdit(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)

    def post(self, request, format=None):
        try:
            with transaction.atomic():

                profile_id = request.user.profile.id
                email_id = request.data["email_id"]
                print("email_id",email_id,type(email_id))
                is_exist_email = Profile.objects.exclude(id=profile_id).filter(email__iexact=email_id).exists()
                print("is_exist_email",is_exist_email)
                if is_exist_email == True:
                    return Response({'request_status': 0,
                            'results':{
                                'msg':'Sorry!,Email id already exists,try with another email id'
                                },
                            },
                            status=419)
                else:
                    return Response({'request_status': 1,
                            'results':{
                                'msg':'success'
                                },
                            },
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise e

class Emailexists(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)

    # @response_modify_decorator_post
    def post(self, request, format=None):
        try:
            with transaction.atomic():
                email_id = request.data["email_id"]
                print("email_id",email_id,type(email_id))
                is_exist_email = Profile.objects.filter(email__iexact=email_id).exists()
                print("is_exist_email",is_exist_email)
                if is_exist_email == True:
                    return Response({'request_status': 0,
                            'results':{
                                'msg':'Sorry!,email-id already exists,try with another email-id'
                                },
                            },
                            status=419)
                else:
                    return Response({'request_status': 1,
                            'results':{
                                'msg':'success'
                                },
                            },
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise e
class phoneexistsProfileEdit(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profile.objects.filter(is_deleted=False)

    def post(self, request, format=None):
        try:
            with transaction.atomic():

                profile_id = request.user.profile.id
                Phone_number = request.data["phone_no"]
                dial_code = request.data["dial_code"]
                print("Phone_number",Phone_number,type(Phone_number))
                is_exist_number = Profile.objects.exclude(id=profile_id).filter(phone__iexact=Phone_number,dial_code=dial_code).exists()
                print("is_exist_number",is_exist_number)
                if is_exist_number == True:
                    return Response({'request_status': 0,
                            'results':{
                                'msg':'Sorry!,mobile number already exists,try with another mobile number'
                                },
                            },
                            status=419)
                else:
                    return Response({'request_status': 1,
                            'results':{
                                'msg':'success'
                                },
                            },
                            status=status.HTTP_200_OK)
        except Exception as e:
            raise e

class PhoneOtpGenerate(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            with transaction.atomic():
                Phone_number = request.data["phone_no"]
                dial_code = request.data["dial_code"]
                dial_cd = dial_code[1:]
                print("Phone_number",Phone_number,"dial_code",dial_code)
                mobile_number = dial_cd+Phone_number
                OTP=TOTPVerification()
                generate_otp = OTP.generate_token()
                if Phone_number and generate_otp:
                    message_data = {
                        'otp':generate_otp,
                        'phone':mobile_number,

                    }
                    sms_class = GlobleSmsSendTxtLocal('OTP-V',[mobile_number])
                    sms_thread = Thread(target = sms_class.sendSMS, args = (message_data,'sms'))
                    sms_thread.start()
                    return Response({'request_status': 1,
                        'results':{
                            'dial_code':dial_code,
                            'Phone_number':Phone_number,
                            # 'otp':generate_otp,
                            'otp':urlsafe_base64_encode(force_bytes(generate_otp))
                            },
                        'msg':'OTP sent, please check your mobile'
                        },
                        status=status.HTTP_200_OK)
        except ValueError as v:
            return v

class EmailOtpGenerate(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            with transaction.atomic():
                email_id = request.data["email_id"]
                print("email_id",email_id)
                OTP=TOTPVerification()
                generate_otp = OTP.generate_token()
                if email_id and generate_otp:
                    #EMAIL VERIFICATION PART 
                    mail_id = email_id
                    if mail_id:
                        mail_data = {
                            'otp':generate_otp,
                            'email_id':email_id,
                        }
                        mail_class = GlobleMailSend('EOTP', [mail_id])
                        mail_thread = Thread(target = mail_class.mailsend, args = (mail_data,))
                        mail_thread.start()
                
                    return Response({'request_status': 1,
                        'results':{
                            'email_id':email_id,
                            # 'otp':generate_otp,
                            'otp':urlsafe_base64_encode(force_bytes(generate_otp))
                            },
                        'msg':'OTP sent, please check your mailid'
                        },
                        status=status.HTTP_200_OK)
        except ValueError as v:
            return v


class AuthCheckerView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset=User.objects.all()   
    authentication_classes = [TokenAuthentication]
    serializer_class = AuthCheckerSerializer
    # @response_modify_decorator_get
    def get(self, request, *args, **kwargs):
        print("request",request.user)
        data={}
        user = request.user
        is_active=  request.user.is_active
        username = request.user.username
        if is_active == True:
            # token = request.headers['Authorization']
            # print("token",token)
            user_detials = Profile.objects.get(user=user)
            # data['token'] = token
            data['username'] = username
            if user_detials.account != 'Company':
                if user_detials.auth_provider != 'Kidsclub':
                    data['user_details']={
                            "user_id":user_detials.user.id,
                            "profile_id":user_detials.id,
                            "user": user_detials.user.username,
                            "account": user_detials.account,
                            "photoUrl": user_detials.photoUrl,
                            "firstname":user_detials.firstname,
                            "lastname": user_detials.lastname,
                            "email": user_detials.email,
                            "dob": user_detials.dob,
                            "gender":user_detials.gender,
                            "phone":user_detials.phone,
                            'is_active':is_active,
                            "country_code":user_detials.country_code.id,
                            "dial_code":user_detials.dial_code,
                            "verified_user_status":{'status_value':user_detials.verified,'status':user_detials.get_verified_display()},
                            "child_count":user_detials.child_count,
                            'subscribed_count':Subscription.objects.filter(subscribe=user_detials.id).\
                            values_list('profile',flat=True).distinct().count()
                        }
                else:
                    data['user_details']={
                            "user_id":user_detials.user.id,
                            "profile_id":user_detials.id,
                            "user": user_detials.user.username,
                            "account": user_detials.account,
                            "image": request.build_absolute_uri(user_detials.image.url) if user_detials.image else None,
                            "firstname":user_detials.firstname,
                            "lastname": user_detials.lastname,
                            "email": user_detials.email,
                            "dob": user_detials.dob,
                            "gender":user_detials.gender,
                            'is_active':is_active,
                            "phone":user_detials.phone,
                            "country_code":user_detials.country_code.id,
                            "dial_code":user_detials.dial_code,
                            "verified_user_status":{'status_value':user_detials.verified,'status':user_detials.get_verified_display()},
                            "child_count":user_detials.child_count,
                            'subscribed_count':Subscription.objects.filter(subscribe=user_detials.id).\
                            values_list('profile',flat=True).distinct().count()
                        }
            else:
                data['user_details']={
                        "user_id":user_detials.user.id,
                        "profile_id":user_detials.id,
                        "user": user_detials.user.username,
                        "account": user_detials.account,
                        "image": request.build_absolute_uri(user_detials.image.url) if user_detials.image else None,
                        "company_name":user_detials.company_name,
                        "email": user_detials.email,
                        "phone":user_detials.phone,
                        'is_active':is_active,
                        "country_code":user_detials.country_code.id,
                        "dial_code":user_detials.dial_code,
                        "verified_user_status":{'status_value':user_detials.verified,'status':user_detials.get_verified_display()},
                        "address":user_detials.address,
                        'subscribed_count':Subscription.objects.filter(subscribe=user_detials.id).\
                            values_list('profile',flat=True).distinct().count()
                    }
            return Response({'result':data,'request_status': 1,'msg': "Success"}, status=status.HTTP_200_OK)
        else:
            LogoutAllView.post(self,request)
            return Response({'result':data,'request_status': 0,
                'msg': "Opss! your account is deactivated please contact at kidsadmin@mykidsclub.com for more details"}, status=status.HTTP_200_OK)


class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)

    @response_modify_decorator_post
    def post(self, request, format=None):
        try:
            data = {}
            # if request.data.get('auth_provider') != None:
            auth_provider = request.data['auth_provider']  

            if auth_provider.lower() == 'kidsclub':
                username = request.data['username']
                password = request.data['password']

            elif auth_provider.lower() == 'facebook' or auth_provider.lower() == 'google':
                username = request.data['username']
                print("auth_provider",auth_provider,'username',username)
                
            elif auth_provider.lower() == 'admin':
                username = request.data['username']
                password = request.data['password']



            with transaction.atomic():

                print("request.data",request.data)
                serializer = AuthTokenSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                print("user",user.is_superuser)
                login_data = login(request, user)
                print("login_data",login_data)
                response = super(LoginView, self).post(request, format=None)
                if user.is_superuser == False:
                    user_detials = self.queryset.get(user=user)
                    data['token'] = response.data['token']
                    data['token_expiry']=response.data['expiry']
                    data['username'] = username
                else:
                    user_detials = User.objects.get(username=user)
                    role = RoleUserMappingTable.objects.filter(user=user_detials.id)
                    menu_details_final=[]
                    if role:
                        role_data= role.get().role
                        role_details={
                            'id':role_data.id,
                            'role_name':role_data.name,
                        }
                        menu_details = RoleMenuMappingTable.objects.filter(role=role_data.id,
                                        is_deleted=False).values('menu','menu__name','menu__url',
                                        'menu__parent_id','menu__icon','is_create','is_read','is_delete','is_edit')
                        
                        for menu in menu_details:
                            if menu['menu__parent_id'] == 0:
                                data_dict={
                                    'id':menu['menu'],
                                    'name':menu['menu__name'],
                                    'url':menu['menu__url'] ,
                                    'icon':menu['menu__icon'],
                                    "linkProps": {
                                        "queryParams": {
                                            "is_create": menu['is_create'],
                                            "is_read": menu['is_read'],
                                            "is_delete": menu['is_delete'],
                                            "is_edit": menu['is_edit']
                                        }
                                    }
                                }

                                menu_details_final.append(data_dict)
                            else:
                                parent_data = AdminMenu.objects.filter(id=menu['menu__parent_id']).values('id','name','url','icon')
                                print("parent_data",parent_data)
    
                                if parent_data:
                                    check_id = parent_data[0]['id']
                                    print("check_id",check_id)
                                    danger_flag = 0
                                    for check_data in menu_details_final:
                                        if check_data['id'] == check_id:
                                            danger_flag=1
                                    if danger_flag == 0 :
                                        child_list=[]
                                        meta_child={}
                                        data_dict=parent_data[0]
                                        child_data = menu_details.filter(menu__parent_id=menu['menu__parent_id']).values('menu','menu__name','menu__url',
                                            'menu__parent_id','menu__icon','is_create','is_read','is_delete','is_edit')
                                        print("child_data",child_data)
                                        for child in child_data:
                                            meta_child={
                                                'id':child['menu'],
                                                'name':child['menu__name'],
                                                'url':child['menu__url'] ,
                                                'icon':child['menu__url'],
                                                "linkProps": {
                                                    "queryParams": {
                                                        "is_create": menu['is_create'],
                                                        "is_read": menu['is_read'],
                                                        "is_delete": menu['is_delete'],
                                                        "is_edit": menu['is_edit']
                                                    }
                                                }
                                            }
                                            child_list.append(meta_child)
                                        data_dict['children']=child_list
                                        if data_dict not in menu_details_final:
                                            menu_details_final.append(data_dict)

                    else:
                        role_details={}
                        menu_details_final=[]

                    data['token'] = response.data['token']
                    data['token_expiry']=response.data['expiry']
                    data['role_details']=role_details
                    data['menu_details']=menu_details_final
                    data['user_details']={
                        'username':username,
                        "user_id":user_detials.id,
                        "firstname":user_detials.first_name,
                        "lastname": user_detials.last_name,
                        "email": user_detials.email,
                        "is_superuser": user_detials.is_superuser,
                    }

                    return Response(data)

                if user_detials.account != 'Company':
                    if user_detials.auth_provider.lower() != 'kidsclub':
                        data['user_details']={
                                "user_id":user_detials.user.id,
                                "profile_id":user_detials.id,
                                "user": user_detials.user.username,
                                "account": user_detials.account,
                                "photoUrl": user_detials.photoUrl,
                                "firstname":user_detials.firstname,
                                "lastname": user_detials.lastname,
                                "email": user_detials.email,
                                "dob": user_detials.dob,
                                "gender":user_detials.gender,
                                "phone":user_detials.phone,
                                "country_code":user_detials.country_code.id,
                                "dial_code":user_detials.dial_code,
                                "verified_user_status":{'status_value':user_detials.verified,'status':user_detials.get_verified_display()},
                                "child_count":user_detials.child_count,
                                'subscribed_count':Subscription.objects.filter(subscribe=user_detials.id).\
                        values_list('profile',flat=True).distinct().count()
                            }
                    else:
                        data['user_details']={
                                "user_id":user_detials.user.id,
                                "profile_id":user_detials.id,
                                "user": user_detials.user.username,
                                "account": user_detials.account,
                                "image": request.build_absolute_uri(user_detials.image.url) if user_detials.image else None,
                                "firstname":user_detials.firstname,
                                "lastname": user_detials.lastname,
                                "email": user_detials.email,
                                "dob": user_detials.dob,
                                "gender":user_detials.gender,
                                "phone":user_detials.phone,
                                "country_code":user_detials.country_code.id,
                                "dial_code":user_detials.dial_code,
                                "verified_user_status":{'status_value':user_detials.verified,'status':user_detials.get_verified_display()},
                                "child_count":user_detials.child_count,
                                'subscribed_count':Subscription.objects.filter(subscribe=user_detials.id).\
                        values_list('profile',flat=True).distinct().count()
                            }

                else:
                    data['user_details']={
                            "user_id":user_detials.user.id,
                            "profile_id":user_detials.id,
                            "user": user_detials.user.username,
                            "account": user_detials.account,
                            "image": request.build_absolute_uri(user_detials.image.url) if user_detials.image else None ,
                            "company_name":user_detials.company_name,
                            "email": user_detials.email,
                            "phone":user_detials.phone,
                            "country_code":user_detials.country_code.id,
                            "dial_code":user_detials.dial_code,
                            "verified_user_status":{'status_value':user_detials.verified,'status':user_detials.get_verified_display()},
                            "address":user_detials.address,
                            'subscribed_count':Subscription.objects.filter(subscribe=user_detials.id).\
                        values_list('profile',flat=True).distinct().count()
                        }
                return Response(data)
                
                
        except Exception as e:
            raise e


class SignupUserView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = SignupAddSerializer

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)

    @response_modify_decorator_get_after_execution
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)

class SignupSubChildUserView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]
    queryset = SubChildProfile.objects.filter(is_deleted=False)
    serializer_class = SignupSubChildUserAddSerializer

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)

    def get_queryset(self):
        parent_profile_id = self.request.user.profile.id if self.request.user.profile.account == 'Parent' else None
        return self.queryset.filter(profile=parent_profile_id)


    @response_modify_decorator_get_after_execution
    def get(self, request, *args, **kwargs):
        return super(self.__class__,self).get(request, *args, **kwargs)

class EditSubChildProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = SubChildProfile.objects.filter(is_deleted=False)
    serializer_class = EditSubChildProfileViewSerializer

    @response_modify_decorator_update
    def put(self, request, *args, **kwargs):
        account = request.user.profile.account
        parent_id = request.user.profile.id
        print("parent_id",parent_id)
        if account == 'Parent':
            child_id = self.kwargs['pk']
            if SubChildProfile.objects.get(id=child_id).profile.id == parent_id:
                firstname= request.data.get('firstname') if request.data.get('firstname') else ""
                lastname= request.data.get('lastname') if request.data.get('lastname') else ""
                dob= request.data.get('dob') if request.data.get('dob') else None
                gender= request.data.get('gender') if request.data.get('gender') else None
                updated_by= request.data.get('updated_by')
                response = super(self.__class__,self).put(request, *args, **kwargs)
                sub_child = SubChildProfile.objects.exclude(id=child_id).filter(firstname__iexact=firstname,lastname__iexact=lastname,is_deleted=False)
                if not sub_child:
                    print("lets seee")
                    sub_child_update = SubChildProfile.objects.filter(id=child_id).update(firstname=firstname,
                                        lastname=lastname,dob=dob,gender=gender,updated_by=updated_by)
                    return response
                else:
                    raise CustomAPIException(None,'Child Name Already exist',status_code=status.HTTP_409_CONFLICT)

            else:
                return Response({'request_status': 0, 'msg': "can't edit,Access denied"}, status=status.HTTP_200_OK)
class ChangePasswordView(generics.UpdateAPIView):
    """
    For changing password.
    password is changing using login user token.
    needs old password and new password,
    check old password is exiest or not
    if exiest than it works
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user_data = self.request.user
            mail_id = user_data.email
            print('user',user_data)
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({'request_status': 0,'result':{'msg': "Old password does not match ..."}}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            LogoutAllView.post(self,request)
            return Response({'request_status': 1, 'result':{'msg': "New Password Save Success..."}}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(generics.ListCreateAPIView):
    """
    Forgot password using phone ,
    otp send , after verification, 
    user can set new password 
    using post method
    """

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer

    @response_modify_decorator_get
    def get(self, request, *args, **kwargs):
        return response

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        user = self.queryset
        if request.data.get('email_id'):
            email_id =request.data['email_id'] 
        else:
            email_id=None
        if request.data.get('phone_no'):
            phone_no =request.data['phone_no'] 
            dial_code=request.data['dial_code']
        else:
            phone_no=None
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']
        try:
            if phone_no and email_id is None:
                user_details_exiest = Profile.objects.get(dial_code=dial_code,phone=phone_no).user.id
            elif phone_no is None and email_id :
                user_details_exiest = Profile.objects.get(email=email_id).user.id

        except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
            raise CustomAPIException(None,'Matching User does not exist !',status_code=status.HTTP_404_NOT_FOUND)
        print("user_details_exiest",user_details_exiest)
        if user_details_exiest :
            if new_password == confirm_password:
                user = user.get(id=user_details_exiest)
                if user.check_password(new_password) == False:
                    user.set_password(new_password)  # set password...
                    user.save()
                else:
                    msg = 'Your new password is similar to old password. Please try with another password.'
                    raise CustomAPIException(None,msg,status_code=status.HTTP_409_CONFLICT)
                # LogoutAllView.post(self,request)
                #print('user_data',user_data.cu_user.password)
            return Response({'request_status': 1,'result':{'msg': "New Password Save Success..."}},status=status.HTTP_200_OK)
        else:
            raise APIException({'request_status': 0,'result':{'msg': "User does not exist."}})

# class SubChildLoginView(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = SubChildProfile.objects.filter(is_deleted=False)

#     @response_modify_decorator_post
#     def post(self, request,*args,**kwargs):
#         try:
#             data = {}                
#             if auth_provider.lower() == 'Subchild':
#                 subchild_userid = request.data['subchild_id']
#                 password = request.data['password']

#             subchild = SubChildProfile.objects.get(id=subchild_userid,is_deleted=False)
#             try:
#                 if request.user.profile.account.lower() == 'parent':
#                     parent_id = request.user.profile.id  

#             except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
#                 raise CustomAPIException(None,'Matching User does not exist !',status_code=status.HTTP_404_NOT_FOUND)
#             if subchild.profile == parent_id:
#                 user_details_exiest = Profile.objects.get(id=parent_id,is_deleted=False).user.id
#                 user = User.objects.get(id=user_details_exiest)
#                 if user.check_password(password) == True:




'''
Login with restauth token : ----  single device 

# class LoginUserView(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = Profile.objects.filter(is_deleted=False)
#     serializer_class = LoginSerializer

#     @response_modify_decorator_post
#     def post(self, request, *args, **kwargs):
#         # response = super(self.__class__,self).post(request, *args, **kwargs)
#         try:
#             data = {}
#             username = request.data['username']
#             password = request.data['password']
#             print("username ",username,"password",password)
#             with transaction.atomic():
#                 if username is (None or "") or password is (None or ""):
#                     print("entered ")
#                     # custom_exception_message(self,None,"Please provide both username and password")
#                     raise ValidationError({
#                         "error":{
#                             'request_status': 0, 
#                             'msg': "Please provide both username and password"
#                             }
#                         }
# )

#                 user = authenticate(username=username, password=password)

#                 print("user",user.first_name)
#                 if not user:
#                      raise CustomAPIException(None,'Invalid Credentials',status_code=status.HTTP_401_UNAUTHORIZED)
#                 else:
#                     token, _ = Token.objects.get_or_create(user=user)
#                     user_detials = self.queryset.get(user=user)
#                     # .values('user','account','image','firstname',
#                     #                                                 'lastname','email','dob','gender','phone','child_count',
#                     #                                                 )
#                     data['token'] = token.key
#                     data['username'] = username
#                     data['user_detials']={
#                             "user": user_detials.user.username,
#                             "account": user_detials.account,
#                             "image": request.build_absolute_uri(user_detials.image.url),
#                             "firstname":user_detials.firstname,
#                             "lastname": user_detials.lastname,
#                             "email": user_detials.email,
#                             "dob": user_detials.dob,
#                             "gender":user_detials.gender,
#                             "phone":user_detials.phone,
#                             "child_count":user_detials.child_count
#                         }
                    

                

#                 return Response(data)
#         except Exception as e:
#             raise e

'''