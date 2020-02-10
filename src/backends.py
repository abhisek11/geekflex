from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from videoservices.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q
from custom_exception_message import *

class EmailandPhoneAuthBackend(ModelBackend):
	"""
	Email Authentication Backend

	Allows a user to sign in using an email or phone/password pair rather than
	a username/password pair.

	"""
 
	def authenticate(self,request,username=None, password=None,**kwargs):
		""" Authenticate a user based on email address or phone number
             as the user name. """
		
		try:
			user_admin = User.objects.filter(username=username,is_superuser=True)
			print("username",user_admin)
			if user_admin:
				if username and password:
					user = User.objects.get(username=username)
				if user.check_password(password) and self.user_can_authenticate(user):
					return user					
			if kwargs['auth_provider'] == 'Kidsclub':
				if username and password:
					user_name = Profile.objects.filter(Q(email=username)| Q(phone=username),auth_provider=kwargs['auth_provider']).values('user__username')
					print("user_name",user_name)
					if user_name:
						account_validation = User.objects.get(username=user_name[0]['user__username'])
						if account_validation.is_active == True:
							user = User.objects.get(username=user_name[0]['user__username'])
							if user.check_password(password) and self.user_can_authenticate(user):
								return user
						else:
							msg = 'Please verify your email to activate account.'
							print("msg",msg)
							# raise serializers.ValidationError(msg, code='authorization')
							raise CustomAPIException(None,msg,status_code=status.HTTP_200_OK)
					else:
						msg = 'Unable to log in with provided credentials.'
						print("msg",msg)
						# raise serializers.ValidationError(msg, code='authorization')
						raise CustomAPIException(None,msg,status_code=status.HTTP_200_OK)
					
						
					
			elif kwargs['auth_provider'] == 'Facebook' or kwargs['auth_provider'] == 'Google': 
				if username and password is None:
					user_name = Profile.objects.filter(Q(email=username)| Q(phone=username),auth_provider=kwargs['auth_provider']).values('user__username')
					print("user_name",user_name)
					if not user_name:
						msg = 'Unable to log in with provided social auth credentials.'
						raise CustomAPIException(None,msg,status_code=444)
					
					user = User.objects.get(username=user_name[0]['user__username'])
					
					# if user.check_password(password) and self.user_can_authenticate(user):
					if self.user_can_authenticate(user):
						return user



		except User.DoesNotExist:
			return None
 
	def get_user(self, user_id):
		""" Get a User object from the user_id. """
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None