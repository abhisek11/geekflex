from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('home/',views.HomeVideoListingView.as_view()),
    path('home/auth/',views.HomeVideoListingAuthView.as_view()),
    path('edit_profile/<pk>/',views.EditProfileView.as_view()),
    path('edit_profile_image/<pk>/',views.EditProfileImageView.as_view()),
    path('edit_sub_child_profile_image/<pk>/',views.EditSubChildProfileImageView.as_view()),
    path('subscribe_channel/',views.SubscribeChannelAddView.as_view()),
    path('profile_or_channel_details/',views.ProfileOrChannelDetailsView.as_view()),
    path('subchild_details/', views.SubChildUserDetailsView.as_view()), 
    path('upload_video/',views.UploadVideoAddView.as_view()),
    path('upload_video_thumpnail_add/',views.UploadVideoThumpnailAddView.as_view()), 
    path('video_list_with_genere/',views.VideoListingGenereView.as_view()),
    path('channel_video_list/',views.ChannelVideoListingView.as_view()),
]
