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
from videoservices.models import *
from rest_framework import mixins
from custom_decorator import *
from rest_framework.views import APIView
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from threading import Thread  # for threading
import datetime
from smsapp.views import *
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from OTPvarify import TOTPVerification
from kidsclub.settings import REDIRECT_URL as redirect_url
from django.shortcuts import render,redirect

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

def phoneexists(request,phone_no):

    Phone_number = phone_no
    is_exist_number = Profile.objects.filter(phone=Phone_number).exists()
    print("is_exist_number",is_exist_number)
    if is_exist_number == True:
        return JsonResponse({'request_status': 0,
                'results':{
                    'msg':'Sorry!,mobile number already exists,try with another mobile number'
                    },
                },
                status=419)
    else:
        return JsonResponse({'request_status': 1,
                'results':{
                    'msg':'success'
                    },
                },
                status=status.HTTP_200_OK)
    



def PhoneOtpGenerate(request,phone_no):

    try:  
        OTP=TOTPVerification()
        Phone_number = phone_no
        generate_otp = OTP.generate_token()
        if Phone_number and generate_otp:
            message_data = {
                'otp':generate_otp,
                'phone':Phone_number,

            }
            sms_class = GlobleSmsSendTxtLocal('OTP-V',[Phone_number])
            sms_thread = Thread(target = sms_class.sendSMS, args = (message_data,'sms'))
            sms_thread.start()
            return JsonResponse({'request_status': 1,
                'results':{
                    'Phone_number':Phone_number,
                    'otp':generate_otp
                    },
                'msg':'OTP sent, please check your mobile'
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
        username = request.user.username
        
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
                        "image": request.build_absolute_uri(user_detials.image.url),
                        "firstname":user_detials.firstname,
                        "lastname": user_detials.lastname,
                        "email": user_detials.email,
                        "dob": user_detials.dob,
                        "gender":user_detials.gender,
                        "phone":user_detials.phone,
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
                    "image": request.build_absolute_uri(user_detials.image.url),
                    "company_name":user_detials.company_name,
                    "email": user_detials.email,
                    "phone":user_detials.phone,
                    "address":user_detials.address,
                    'subscribed_count':Subscription.objects.filter(subscribe=user_detials.id).\
                        values_list('profile',flat=True).distinct().count()
                }
        return Response({'result':data,'request_status': 1,'msg': "Success"}, status=status.HTTP_200_OK)
    

class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)

    @response_modify_decorator_post
    def post(self, request, format=None):
        try:
            data = {}
            auth_provider = request.data['auth_provider']
            if auth_provider == 'Kidsclub':
                username = request.data['username']
                password = request.data['password']

            elif auth_provider == 'Facebook' or auth_provider == 'Google':
                username = request.data['username']
                print("auth_provider",auth_provider,'username',username)

            with transaction.atomic():

                print("request.data",request.data)
                serializer = AuthTokenSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                login_data = login(request, user)
                response = super(LoginView, self).post(request, format=None)
                user_detials = self.queryset.get(user=user)
                data['token'] = response.data['token']
                data['token_expiry']=response.data['expiry']
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
                                "image": request.build_absolute_uri(user_detials.image.url),
                                "firstname":user_detials.firstname,
                                "lastname": user_detials.lastname,
                                "email": user_detials.email,
                                "dob": user_detials.dob,
                                "gender":user_detials.gender,
                                "phone":user_detials.phone,
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
                            "image": request.build_absolute_uri(user_detials.image.url),
                            "company_name":user_detials.company_name,
                            "email": user_detials.email,
                            "phone":user_detials.phone,
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
                return super().put(request, *args, **kwargs)
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
        phone_no =request.data['phone_no'] 
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password'] 
        try:
            user_details_exiest = Profile.objects.get(phone=phone_no).user.id
        except(TypeError, ValueError, OverflowError, User.DoesNotExist): 
            raise CustomAPIException(None,'Matching User does not exist !',status_code=status.HTTP_404_NOT_FOUND)
        print("user_details_exiest",user_details_exiest)
        if user_details_exiest :
            if new_password == confirm_password:
                user = user.get(id=user_details_exiest)
                user.set_password(new_password)  # set password...
                user.save()
                # LogoutAllView.post(self,request)
                #print('user_data',user_data.cu_user.password)
            return Response({'request_status': 1,'result':{'msg': "New Password Save Success..."}},status=status.HTTP_200_OK)
        else:
            raise APIException({'request_status': 0,'result':{'msg': "User does not exist."}})

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