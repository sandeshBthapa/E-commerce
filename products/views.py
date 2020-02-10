from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404

from cart.models import Cart
from .models import Product

# Create your views here.
class ProductFeaturedListView(ListView):
    # queryset = Product.objects.all()
    model = Product
    template_name = "products/plist.html"
    context_object_name = "product_list"
    def get_queryset(self):   
        request = self.request
        return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.featured()
    template_name = "products/pdetail.html"
    context_object_name = "product"
    # def get_queryset(self, *args, **kwargs):
    #     return Product.objects.featured()

class ProductListView(ListView): 
    # queryset = Product.objects.all()
    model = Product
    template_name = "products/plist.html"
    context_object_name = "product_list"
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context) #object_list
    #     return context

    #second way of doing
    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {'product_list':queryset}
    return render(request, "products/plist.html", context)

class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    model = Product
    template_name = "products/pdetail.html"
    context_object_name = "product"
    # def get_context_data(self,**kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(context)
    #     return context

    #second way of doing
    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404("Product doesn't exitst.")
    #     return instance

    #third way of doing
    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(id=pk)


def product_detail_view(request,pk=None):
    #first way of doing
    # instance = get_object_or_404(Product, id=pk)  

    #second way of doing
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print(f"No product with id = {pk}")
    #     raise Http404("Product does not exist !")

    #third way of doing
    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist.")

    #fourth way of doing
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist.")

    context = {'product':instance}
    return render(request, "products/pdetail.html", context)

class ProductDetailSlugView(DetailView):
    # queryset = Product.objects.all()
    model = Product 
    template_name = "products/pdetail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, _ = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    # def get_object(self, *args, **kwargs):
    #     #request = self.request
    #     slug = self.kwargs.get('slug')
    #     # instance = get_object_or_404(Product, slug=slug, active=True)
    #     try:
    #         instance = Product.objects.get(slug=slug, active=True)
    #     except Product.DoesNotExist:
    #         raise Http404(f"Product with slug { slug } does not exist !")
    #     except Product.MultipleObjectsReturned:
    #         qs = Product.objects.filter(slug = slug , active = True)
    #         instance = qs.first()
    #     except:
    #         raise Http404("Error occured")
    #     return instance