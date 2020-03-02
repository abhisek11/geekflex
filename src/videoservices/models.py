from django.contrib.auth.models import User
from django.db import models
from datetime import date
import time

class Genere(models.Model):
    name =  models.CharField(max_length=100,blank=True,null=True)
    url = models.CharField( max_length=500,blank=True,null=True)
    icon = models.CharField( max_length=500,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='g_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='g_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='g_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Genere'

class CountryCode(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    dial_code = models.CharField(max_length=10,blank=True,null=True)
    code=models.CharField(max_length=4,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='c_c_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='c_c_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='c_c_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'countrycode'

class Profile(models.Model):

    AUTH_TYPES = (
        ('Kidsclub','Kidsclub'),
        ('Facebook','Facebook'),
        ('Google','Google'),
    )
    VERIFIED_TYPES = (
        (0,'Not Verified'),
        (1,'Pending'),
        (2,'Verified'),
        (3,'rejected'),
    )
    ACCOUNT_TYPES = (
        ('Individual', 'Individual'),
        ('Parent','Parent'),
        ('Child','Child'),
        ('Company', 'Company'),
    )
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Other')
    )
    auth_provider = models.CharField(default='Kidsclub', choices=AUTH_TYPES,max_length=20)
    verified = models.IntegerField(default=0, choices=VERIFIED_TYPES)
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    account = models.CharField(default='Individual', choices=ACCOUNT_TYPES,max_length=20)
    photoUrl = models.CharField( max_length=1000,blank=True,null=True)
    image = models.ImageField(upload_to="avatars", default="avatars/None/default_avatar.png")
    firstname = models.CharField(blank=True, max_length=30,null=True)
    lastname = models.CharField(blank=True, max_length=150,null=True)
    company_name = models.CharField(blank=True, max_length=150,null=True)
    address = models.CharField(blank=True, max_length=250,null=True)
    email = models.EmailField(blank=True,null=True)
    dob = models.DateField(default=date(1000, 1, 1))
    gender = models.CharField(blank=True, max_length=1, choices=GENDER)
    country_code = models.ForeignKey(CountryCode,on_delete=models.CASCADE,blank=True,null=True)
    dial_code= models.CharField(blank=True, max_length=4,null=True)
    phone = models.CharField(blank=True, max_length=10,null=True)
    child_count = models.IntegerField(default=0)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='p_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # if self.account == 'Parent':
        #     self.child_count = 2 
        #     self.save()
        return str(self.id)

    class Meta:
        db_table = 'Profile'

class SubChildProfile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Other')
    )
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    firstname = models.CharField(blank=True, max_length=30)
    lastname = models.CharField(blank=True, max_length=150)
    dob = models.DateField(default=date(1000, 1, 1))
    image = models.ImageField(upload_to="avatars", default="avatars/None/default_avatar.png")
    gender = models.CharField(blank=True, max_length=1, choices=GENDER)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='s_c_p_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='s_c_p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='s_c_p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'SubChildProfile'


class Video(models.Model):
    AGE_RANGE = (
        ('3-12', '3-12'),
        ('13-17','13-17'),
        ('18+ or above','18+ or above'),
    )
    channel = models.ForeignKey(Profile, on_delete=models.CASCADE,blank=True,null=True)
    video = models.FileField(upload_to="videos")
    title = models.CharField(max_length=46,blank=True,null=True)
    description = models.TextField(max_length=3000,blank=True,null=True)
    category = models.ForeignKey(Genere, on_delete=models.CASCADE,blank=True,null=True)
    private_video = models.BooleanField(default=False)
    featured_video = models.BooleanField(default=False)
    private_code = models.CharField(max_length=10,blank=True,null=True)
    term_and_conditions = models.BooleanField(default=False)
    age_range = models.CharField(default='21+ or above', choices=AGE_RANGE,max_length=20)
    is_admin_reviewed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='v_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Video'

class VideoTags(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE,blank=True,null=True)
    tags = models.CharField(max_length=200,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='v_t_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='v_t_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='v_t_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'videotags'

class VideoThumbnailDocuments(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE,blank=True,null=True)
    thumbnail = models.FileField(upload_to="thumpnails", default="thumpnail/None/default_thump.png")
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='v_t_d_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='v_t_d_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='v_t_d_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'VideoThumbnailDocuments'

class VideoViews(models.Model):
    MOOD_TYPE =(
        ('Happy','Happy'),
        ('Sad','Happy'),
        ('Angry','Angry'),
    )
    Profile = models.IntegerField(default=0)
    video = models.ForeignKey(Video, on_delete=models.CASCADE,blank=True,null=True)
    mood = models.CharField(default='Happy', choices=MOOD_TYPE,max_length=20,blank=True, null=True)
    view_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='v_v_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='v_v_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='v_v_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'VideoViews'


class Subscription(models.Model):
    profile= models.ForeignKey(Profile,on_delete=models.CASCADE,
                                blank=True, null=True,related_name='s_channel')
    subscribe = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True,
                                    null=True,related_name='s_subscribe_profile')
    is_subscribed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='s_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='s_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='s_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Subscription'

class Notifications(models.Model):
    subscribed= models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, null=True)
    notify = models.ForeignKey(Video,on_delete=models.CASCADE, blank=True, null=True)
    is_notified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='n_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='n_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='n_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Notifications'

# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     text = models.TextField(max_length=1000, default="no-review")
#     rating = models.DecimalField(max_digits=2, decimal_places=1, default=1.0)
#     approvedBy = models.TextField(default="")
#     disapprovedBy = models.TextField(default="")

#     def __str__(self):
#         return self.user.username+" "+self.text
