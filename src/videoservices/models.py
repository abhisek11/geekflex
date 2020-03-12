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
        ('Subchild','Subchild'),
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
        ('Subchild','Subchild'),
    )
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Other')
    )
    auth_provider = models.CharField(default='Kidsclub', choices=AUTH_TYPES,max_length=20)
    verified = models.IntegerField(default=0, choices=VERIFIED_TYPES)
    parent_id = models.IntegerField(default=0)
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
    bio = models.TextField(blank=True,null=True) #for future channel about section 
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

# class SubChildProfile(models.Model):
#     GENDER = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O','Other')
#     )
#     profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
#     firstname = models.CharField(blank=True, max_length=30)
#     lastname = models.CharField(blank=True, max_length=150)
#     dob = models.DateField(default=date(1000, 1, 1))
#     image = models.ImageField(upload_to="avatars", default="avatars/None/default_avatar.png")
#     gender = models.CharField(blank=True, max_length=1, choices=GENDER)
#     is_deleted = models.BooleanField(default=False)
#     created_by = models.ForeignKey(User, related_name='s_c_p_created_by',
#                                    on_delete=models.CASCADE, blank=True, null=True)
#     owned_by = models.ForeignKey(User, related_name='s_c_p_owned_by',
#                                  on_delete=models.CASCADE, blank=True, null=True)
#     updated_by = models.ForeignKey(User, related_name='s_c_p_updated_by',
#                                    on_delete=models.CASCADE, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.id)

#     class Meta:
#         db_table = 'SubChildProfile'


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
    duration = models.IntegerField(default=0)
    private_code = models.CharField(max_length=10,blank=True,null=True)
    term_and_conditions = models.BooleanField(default=False)
    age_range = models.CharField(default='21+ or above', choices=AGE_RANGE,max_length=20)
    is_admin_reviewed = models.BooleanField(default=False)
    is_admin_published = models.BooleanField(default=False)
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

class VideoSearchHistory(models.Model):
    Profile = models.IntegerField(default=0)
    Search_keys = models.CharField(max_length=200,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='v_s_h_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='v_s_h_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='v_s_h_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'video_search_history'


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


class MobileDevice(models.Model):
    participant = models.OneToOneField(User, related_name='device', on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=(('iOS', 'iOS'), ('Android', 'Android'),))
    token = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='md_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='md_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='md_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'MobileDevice'
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

#******************PAYMENTS SECTION*****************************************
class PaymentPlan(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    description = models.CharField(max_length=500,blank=True,null=True)
    amount = models.IntegerField(blank=True,null=True,default=0)
    validity = models.IntegerField(blank=True,null=True)
    active_status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='pa_p_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='pa_p_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='pa_p_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'payment_plan'

class PlanBenifits(models.Model):
    plan= models.ForeignKey(PaymentPlan,on_delete=models.CASCADE, blank=True, null=True)
    extra_child = models.IntegerField(blank=True,null=True,default=0)
    featured_video = models.BooleanField(default=False)
    featured_video_display_days = models.IntegerField(blank=True,null=True,default=0)
    ads_blocking = models.BooleanField(default=False)
    child_report_generation = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='pa_b_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='pa_b_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='pa_b_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'plan_benifits'


class UserPaymentTransaction(models.Model):
    profile= models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, null=True)
    plan= models.ForeignKey(PaymentPlan,on_delete=models.CASCADE, blank=True, null=True)
    payed_amount = models.IntegerField(blank=True,null=True)
    status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200,blank=True,null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='upt_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='upt_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='upt_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'user_payment_transaction'


# class Review(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     text = models.TextField(max_length=1000, default="no-review")
#     rating = models.DecimalField(max_digits=2, decimal_places=1, default=1.0)
#     approvedBy = models.TextField(default="")
#     disapprovedBy = models.TextField(default="")

#     def __str__(self):
#         return self.user.username+" "+self.text

class Help(models.Model):
    name = models.CharField( max_length=200)
    email = models.EmailField( max_length=200)
    mobile = models.CharField(max_length=11)
    query = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='h_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='h_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='h_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'help'

class Feedback(models.Model):
    name = models.CharField( max_length=200)
    email = models.EmailField( max_length=200)
    mobile = models.CharField(max_length=11)
    feedback = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='f_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='f_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='f_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'feedback'

class Sponsors(models.Model):
    name = models.CharField( max_length=200)
    email = models.EmailField( max_length=200)
    mobile = models.CharField(max_length=11)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='sp_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='sp_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='sp_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'sponsers'

class Service(models.Model):
    name = models.CharField( max_length=200)
    email = models.EmailField( max_length=200)
    mobile = models.CharField(max_length=11)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='ser_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='ser_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='ser_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'service'

class Career(models.Model):
    name = models.CharField( max_length=200)
    email = models.EmailField( max_length=200)
    mobile = models.CharField(max_length=11)
    message = models.TextField()
    address = models.CharField(max_length=500)
    doc = models.FileField(upload_to="docs")
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='car_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='car_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='car_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'career'

class About(models.Model):
    title = models.CharField( max_length=200)
    description = models.TextField()
    doc = models.FileField(upload_to="docs", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='ab_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='ab_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='ab_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'about'

class TermsConditions(models.Model):
    title = models.CharField( max_length=200)
    description = models.TextField()
    doc = models.FileField(upload_to="docs", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='tc_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='tc_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='tc_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'terms_conditions'

class PrivacyPolicy(models.Model):
    title = models.CharField( max_length=500)
    description = models.TextField()
    doc = models.FileField(upload_to="docs", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='pp_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='pp_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='pp_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'privacy_policy'

class WatchTimerLog(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    duration = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='wtl_created_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name='wtl_owned_by',
                                 on_delete=models.CASCADE, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='wtl_updated_by',
                                   on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'watchTimerLog'

