from django.conf import settings
from django.db import models


MEMBERSHIP_CHOICES = (
    ('Enterprice','Enterprice'),
    ('Professional','Professional'),
    ('Free','Free')
)
class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
                        choices=MEMBERSHIP_CHOICES,
                        max_length=30,
                        default='Free')
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return str(self.membership_type)
    class Meta:
        db_table = 'membership'

class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'user_membership'