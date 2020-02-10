from django.urls import path, include
from . import views

app_name = "cart"
urlpatterns = [
    path('cart/', views.cart_home, name='home'),
    path('cart/update/', views.cart_update, name='update'),
    path('checkout/', views.checkout_home, name='checkout'),
]
