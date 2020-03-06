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


@admin.register(Help)
class Help(admin.ModelAdmin):
    list_display = [field.name for field in Help._meta.fields]

@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    list_display = [field.name for field in Feedback._meta.fields]

@admin.register(Sponsors)
class Sponsors(admin.ModelAdmin):
    list_display = [field.name for field in Sponsors._meta.fields]

@admin.register(Service)
class Service(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.fields]

@admin.register(VideoSearchHistory)
class VideoSearchHistory(admin.ModelAdmin):
    list_display = [field.name for field in VideoSearchHistory._meta.fields]

@admin.register(Career)
class Career(admin.ModelAdmin):
    list_display = [field.name for field in Career._meta.fields]

@admin.register(About)
class About(admin.ModelAdmin):
    list_display = [field.name for field in About._meta.fields]

@admin.register(Terms_conditions)
class Terms_conditions(admin.ModelAdmin):
    list_display = [field.name for field in Terms_conditions._meta.fields]

@admin.register(Privacy_policy)
class Privacy_policy(admin.ModelAdmin):
    list_display = [field.name for field in Privacy_policy._meta.fields]

@admin.register(WatchTimerLog)
class WatchTimerLog(admin.ModelAdmin):
    list_display = [field.name for field in WatchTimerLog._meta.fields]



