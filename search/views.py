from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404

from products.models import Product


# Create your views here.
class SearchProductView(ListView):
    template_name = "search/view.html"
    context_object_name = "product_list"
    def get_queryset(self,*args, **kwargs):
        request = self.request
        # print(request.GET)
        query = request.GET.get('q', None)
        print("Query value is : ", query)
        if query is not None:

            # 1st way
            # return Product.objects.filter(title__icontains=query)
            # 2nd way
            # lookups = Q(title__icontains=query) | Q(description__icontains=query)
            # return Product.objects.filter(lookups).distinct()
            # 3rd way
            return Product.objects.search(query)   
        # return Product.objects.none()
        return Product.objects.featured()
    #third way of doing
    # def get_context_data(self, *args, **kwargs):
    #     context = super(SearchProductView,self).get_context_data(*args, **kwargs)
    #     query = self.request.GET.get('q')
    #     context['query'] = query
    #     # SearchQuery.objects.create(query=query) # To later analyze queries by the user.
    #     return context
    