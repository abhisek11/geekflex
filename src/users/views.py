from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.exceptions import ValidationError
from custom_exception_message import *
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import generics
from videoservices.serializers import *
from users.serializers import *
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
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
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginView(KnoxLoginView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)

    @response_modify_decorator_post
    def post(self, request, format=None):
        try:
            data = {}
            username = request.data['username']
            password = request.data['password']
            with transaction.atomic():

                # print('username',username,'password',password)
                serializer = AuthTokenSerializer(data=request.data)
                # print("serializer",serializer)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                login_data = login(request, user)
                response = super(LoginView, self).post(request, format=None)
                # print("logindata",login_data)
                # print("response",response.data)
                user_detials = self.queryset.get(user=user)
                data['token'] = response.data['token']
                data['username'] = username
                data['user_detials']={
                        "user": user_detials.user.username,
                        "account": user_detials.account,
                        "image": request.build_absolute_uri(user_detials.image.url),
                        "firstname":user_detials.firstname,
                        "lastname": user_detials.lastname,
                        "email": user_detials.email,
                        "dob": user_detials.dob,
                        "gender":user_detials.gender,
                        "phone":user_detials.phone,
                        "child_count":user_detials.child_count
                    }
                    

                

                return Response(data)
                # return super(LoginView, self).post(request, format=None)
                
                
        except Exception as e:
            raise e


class SignupUserView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = SignupAddSerializer

    @response_modify_decorator_get
    def get(self, request, *args, **kwargs):
        return response

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)

class LoginUserView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.filter(is_deleted=False)
    serializer_class = LoginSerializer

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        # response = super(self.__class__,self).post(request, *args, **kwargs)
        try:
            data = {}
            username = request.data['username']
            password = request.data['password']
            print("username ",username,"password",password)
            with transaction.atomic():
                if username is (None or "") or password is (None or ""):
                    print("entered ")
                    # custom_exception_message(self,None,"Please provide both username and password")
                    raise ValidationError({
                        "error":{
                            'request_status': 0, 
                            'msg': "Please provide both username and password"
                            }
                        }
)

                user = authenticate(username=username, password=password)

                print("user",user.first_name)
                if not user:
                     raise CustomAPIException(None,'Invalid Credentials',status_code=status.HTTP_401_UNAUTHORIZED)
                else:
                    token, _ = Token.objects.get_or_create(user=user)
                    user_detials = self.queryset.get(user=user)
                    # .values('user','account','image','firstname',
                    #                                                 'lastname','email','dob','gender','phone','child_count',
                    #                                                 )
                    data['token'] = token.key
                    data['username'] = username
                    data['user_detials']={
                            "user": user_detials.user.username,
                            "account": user_detials.account,
                            "image": request.build_absolute_uri(user_detials.image.url),
                            "firstname":user_detials.firstname,
                            "lastname": user_detials.lastname,
                            "email": user_detials.email,
                            "dob": user_detials.dob,
                            "gender":user_detials.gender,
                            "phone":user_detials.phone,
                            "child_count":user_detials.child_count
                        }
                    

                

                return Response(data)
        except Exception as e:
            raise e

class Logout(APIView):
    """
        View for user logout
        And delete auth_token
        Using by login user token
        """

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({'request_status': 0, 'msg': "Logout Success..."}, status=status.HTTP_200_OK)