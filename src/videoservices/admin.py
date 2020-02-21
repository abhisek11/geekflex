from django.contrib import admin
from videoservices.models import *

# Register your models here.
@admin.register(Genere)
class Genere(admin.ModelAdmin):
    list_display = [field.name for field in Genere._meta.fields]

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

@admin.register(SubChildProfile)
class SubChildProfile(admin.ModelAdmin):
    list_display = [field.name for field in SubChildProfile._meta.fields]

@admin.register(Notifications)
class Notifications(admin.ModelAdmin):
    list_display = [field.name for field in Notifications._meta.fields]

@admin.register(Subscription)
class Subscription(admin.ModelAdmin):
    list_display = [field.name for field in Subscription._meta.fields]

@admin.register(Video)
class Video(admin.ModelAdmin):
    list_display = [field.name for field in Video._meta.fields]

@admin.register(VideoViews)
class VideoViews(admin.ModelAdmin):
    list_display = [field.name for field in VideoViews._meta.fields]

@admin.register(VideoThumbnailDocuments)
class VideoThumbnailDocuments(admin.ModelAdmin):
    list_display = [field.name for field in VideoThumbnailDocuments._meta.fields]

@admin.register(CountryCode)
class CountryCode(admin.ModelAdmin):
    list_display = [field.name for field in CountryCode._meta.fields]
    search_fields = ('name',)

@admin.register(VideoTags)
class VideoTags(admin.ModelAdmin):
    list_display = [field.name for field in VideoTags._meta.fields]

