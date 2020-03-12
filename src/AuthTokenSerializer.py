from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from custom_exception_message import *


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=False
    )
    auth_provider = serializers.CharField(required=False)
    def validate(self, attrs):
        print("attrs",attrs)
        
        auth_provider = attrs.get('auth_provider')
        # print("auth_provider",auth_provider)
        
        #changes done by abhisek singh 
        if auth_provider.lower()== 'admin':
            username = attrs.get('username')
            password = attrs.get('password')
            # if username is  and password :
            print("username",username,'password',password)
            if username and password :
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password,auth_provider=auth_provider)

                # The authenticate call simply returns None for is_active=False
                # users. (Assuming the default ModelBackend authentication
                # backend.)
                if not user:
                    msg = _('Unable to log in with provided credentials.')
                    # raise serializers.ValidationError(msg, code='authorization')
                    raise CustomAPIException(None,msg,status_code=status.HTTP_200_OK)
            else:
                msg = _('Provided credentials with username and password cannot be blank .')
                raise CustomAPIException(None,msg,status_code=status.HTTP_400_BAD_REQUEST)

        elif auth_provider.lower()== 'kidsclub':
            username = attrs.get('username')
            password = attrs.get('password')
            # if username is  and password :
            print("username",username,'password',password,'auth_provider',auth_provider)
            if username and password :
            # if (username is not None or username is not "") and (password is not None or password is not ""):

                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password,auth_provider=auth_provider)

                # The authenticate call simply returns None for is_active=False
                # users. (Assuming the default ModelBackend authentication
                # backend.)
                if not user:
                    msg = _('Unable to log in with provided credentials.')
                    # raise serializers.ValidationError(msg, code='authorization')
                    raise CustomAPIException(None,msg,status_code=status.HTTP_200_OK)
            else:
                msg = _('Provided credentials with username and password cannot be blank .')
                raise CustomAPIException(None,msg,status_code=status.HTTP_400_BAD_REQUEST)
        
        elif auth_provider.lower()== 'subchild':
            username = attrs.get('username')
            password = attrs.get('password')
            # if username is  and password :
            print("username",username,'password',password,'auth_provider',auth_provider)
            if username and password :
            # if (username is not None or username is not "") and (password is not None or password is not ""):

                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password,auth_provider=auth_provider)
                print("user",user)
                # The authenticate call simply returns None for is_active=False
                # users. (Assuming the default ModelBackend authentication
                # backend.)
                if not user:
                    msg = _('Unable to log in with provided credentials.')
                    # raise serializers.ValidationError(msg, code='authorization')
                    raise CustomAPIException(None,msg,status_code=status.HTTP_200_OK)
            else:
                msg = _('Provided credentials with username and password cannot be blank .')
                raise CustomAPIException(None,msg,status_code=status.HTTP_400_BAD_REQUEST)

        elif auth_provider.lower() == 'facebook' or auth_provider.lower() == 'google':
            username = attrs.get('username')
            if username :

                user = authenticate(request=self.context.get('request'),
                                    username=username,auth_provider=auth_provider)

                # The authenticate call simply returns None for is_active=False
                # users. (Assuming the default ModelBackend authentication
                # backend.)
                if not user:
                    msg = _('Unable to log in with provided credentials.')
                    # raise serializers.ValidationError(msg, code='authorization')
                    raise CustomAPIException(None,msg,status_code=status.HTTP_200_OK)
                
        else:
            msg = _('Must include "username" and "password".')
            # raise serializers.ValidationError(msg, code='authorization')
            raise ValidationError({
                            "error":{
                            'request_status': 0, 
                            'msg': msg
                            }
                        })
        

        attrs['user'] = user
        return attrs