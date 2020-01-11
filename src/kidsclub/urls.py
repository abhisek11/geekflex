from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# import django.views.defaults
from django.contrib import admin

from django.conf.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('videoservices.urls')),
    path('',include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
elif getattr(settings, 'FORCE_SERVE_STATIC', True):
    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False
