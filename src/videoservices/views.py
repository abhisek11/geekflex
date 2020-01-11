from django.shortcuts import render
from rest_framework import generics
from videoservices.serializers import *
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


class UploadVideoAddView(generics.ListCreateAPIView,mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    queryset = Video.objects.filter(is_deleted=False)
    serializer_class = UploadVideoAddSerializer
    # pagination_class = CSPageNumberPagination

    @response_modify_decorator_get
    def get(self, request, *args, **kwargs):
        return response

    @response_modify_decorator_post
    def post(self, request, *args, **kwargs):
        return super(self.__class__,self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        updated_by=request.user.id
        title=request.data['title'] if request.data['title'] else None
        tags=request.data['tags']  if request.data['tags'] else None
        description=request.data['description']  if request.data['description'] else None
        category=request.data['category']  if request.data['category'] else None
        private_video=request.data['private_video']  if request.data['private_video'] else False
        private_code=request.data['private_code']  if request.data['private_code'] else None
        term_and_conditions=request.data['term_and_conditions']  if request.data['term_and_conditions'] else False
        age_range=request.data['age_range']  if request.data['age_range'] else '21+ or above'

        vid_id = self.request.query_params.get('vid_id', None)
        video_details_update = Video.objects.filter(id=vid_id,is_deleted=False).\
                                update(title=title,tags=tags,description=description,
                                category=category,private_video=private_video,private_code=private_code,
                                term_and_conditions=term_and_conditions,age_range=age_range,updated_by=updated_by)
        print("video_details_update",type(video_details_update))
        if video_details_update:
            return Response({'results': Video.objects.filter(id=vid_id,is_deleted=False).values(),
                                'msg': 'success',
                                "request_status": 1})
        else:
            return Response({'results': [],
                            'msg': 'fail',
                            "request_status": 0})