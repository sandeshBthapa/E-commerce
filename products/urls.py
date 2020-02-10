from django.urls import path, include
from . import views
from .views import (
    ProductListView, 
    ProductDetailView, 
    ProductFeaturedListView,
    ProductFeaturedDetailView,
    ProductDetailSlugView,
    )

app_name = "products"
urlpatterns = [
    # path('logout/', views.logout_and_redirect, name='logout'),
    path('products/', ProductListView.as_view(), name="list"),
    path('products-func/', views.product_list_view ),

    path('products/<slug:slug>/', ProductDetailSlugView.as_view(), name="detail_from_slug"),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
    # path('products-func/<int:pk>/', views.product_detail_view ),

    path('featured/', ProductFeaturedListView.as_view()),
    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
]
