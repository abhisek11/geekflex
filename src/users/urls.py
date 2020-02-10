from users import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from knox import views as knox_views
from django.conf import settings




urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #***************SOCIAL AUTH************************************************************
    path('api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    #**************************************************************************************
    path('signup/', views.SignupUserView.as_view()), #WITH EMAIL VERIFICATION 
    path('signup_for_subchild/', views.SignupSubChildUserView.as_view()), 
    path('edit_for_subchild/<pk>/', views.EditSubChildProfileView.as_view()), 
    path('activate/<uidb64>/',views.activate, name='activate'), #ACTIVATE ACCOUNT AFTER EMAIL VERIFY AUTOMATICALLY
    path('phone_number_verify/<phone_no>/',views.PhoneOtpGenerate, name='generate_otp'),
    path('phone_number_exists_or_not/<phone_no>/',views.phoneexists),

    
    ###################### Multi session Login Logout #####################################
    path('auth_checker/', views.AuthCheckerView.as_view(), name='auth_checker'),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('change_password/', views.ChangePasswordView.as_view()),
    path('forgot_password/', views.ForgotPasswordView.as_view()),

]