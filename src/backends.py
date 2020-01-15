from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from videoservices.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import When, Case, Value, CharField, IntegerField, F, Q

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
			if username and password:
				print("username",username)
				if username.lower() == 'admin':

					user = User.objects.get(username=username)
				else:
					user_name = Profile.objects.get(Q(email=username)| Q(phone=username)).user
					user = User.objects.get(username=user_name)
				if user.check_password(password) and self.user_can_authenticate(user):
					return user
		except User.DoesNotExist:
			return None
 
	def get_user(self, user_id):
		""" Get a User object from the user_id. """
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None