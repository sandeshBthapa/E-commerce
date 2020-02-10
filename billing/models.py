from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    # customer_id in Stripe or Braintree

    def __str__(self):
        return self.email
    
# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("Actual API REQUEST send to Stripe or Paypal")
#         instance.customer_id = newID
#         instance.save()

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)