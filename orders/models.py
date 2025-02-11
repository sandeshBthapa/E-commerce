import math
from django.db import models
from django.db.models.signals import pre_save,post_save

from daraz.utils import unique_order_id_generator
from cart.models import Cart
from billing.models import BillingProfile

# Create your models here.
ORDER_STATUS_CHOICES=(
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"), 
)
class Order(models.Model):
    order_id        = models.CharField(max_length=120, blank=True, unique=True)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    # shipping_address
    # billing_address
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status          = models.CharField(max_length=120, default="created", choices=ORDER_STATUS_CHOICES)
    shipping_total  = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total           = models.DecimalField(default=0.0, max_digits=100, decimal_places=2)
    active          = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id
    
    def update_total(self):
        new_total = math.fsum([self.cart.total, self.shipping_total ]) 
        self.total = format(new_total, ".2f")
        self.save()
        return new_total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        cart_total = cart_obj.total
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.exists() and qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
post_save.connect(post_save_order, sender=Order)

#generate the order_id
#generate the order_total