from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from daraz.utils import unique_slug_generator
from products.models import Product
# Create your models here.

class Tag(models.Model):
    title       = models.CharField(max_length=100)
    slug        = models.SlugField(blank=True)
    timestamp   = models.DateField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField("products.Product", blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "tags"
    
def tags_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tags_pre_save_receiver, sender=Tag)