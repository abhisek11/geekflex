from users import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from knox import views as knox_views




urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('signup/', views.SignupUserView.as_view()),
    path('login/', views.LoginUserView.as_view()),
    path('logout/', views.Logout.as_view()),
    path('login_knox/', views.LoginView.as_view(), name='knox_login'),
    path('logout_knox/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

]