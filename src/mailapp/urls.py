from mailapp import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('mail_send/', views.MailSendApiView.as_view()),
]