from django.db.models import Q
from django.db import models
from django.urls import reverse
import os
import random
from django.db.models.signals import pre_save, post_save

from daraz.utils import unique_slug_generator

# Create your models here.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    name = "".join([c for c in name if c.isalpha() or c.isdigit()]).rstrip()[:30]
    return  (name, ext)

def upload_image_path(self, filename):
    print(self, filename)
    randomInt = random.randint(1,4294967296)
    name , ext = get_filename_ext(filename)
    final_filename = f'{randomInt}{name}{ext}'
    print(final_filename, "---", name, "----", ext)
    return f'products/images/product_images/{final_filename}'

class ProductQuerySet(models.query.QuerySet):
    def active(self):  # Product.objects.all().active()
        return self.filter(active=True)
    def featured(self): # Product.objects.all().featured()
        return self.filter(featured=True, active=True)
    def search(self, query):
        lookups = ( 
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(price__icontains=query) |  
            Q(tag__title__icontains=query)
        )
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self): # get_queryset() means Product.objects !!
        return ProductQuerySet(self.model, using=self._db)

    def get_by_id(self,id): # Product.objects.get_by_id(id)
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def featured(self): # Product.objects.featured()
        # return self.get_queryset().filter(featured=True)
        return self.get_queryset().featured()
        
    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().active().search(query)
        

class Product(models.Model): 
    title       = models.CharField(max_length=100)
    slug        = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,max_digits=10)
    # image     = models.FileField(upload_to='products/images/product_images/', null=True, blank=True)
    # image     = models.FileField(upload_to= upload_image_path , null=True, blank=True)
    image       = models.ImageField(upload_to= upload_image_path , null=True, blank=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)


    objects = ProductManager()

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        # return f"/products/{self.pk}"
        # return f"/products/{self.slug}"
        # return reverse("product_detail", kwargs={"pk": self.pk})
        return reverse("products:detail_from_slug", kwargs={"slug": self.slug})
        
    @property
    def name(self):
        return self.title
        
    class Meta:
        db_table = 'product'


# make slug from title of the product if the value of slug is not given explicitely in the form. 
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)