from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    # r'^login/$' intead of 'login/' was used in previous versions of django !!
    path('register/', views.register_page, name='register'),
    # path('logout/', views.logout_and_redirect, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/guest', views.guest_register_view, name='guest_register'),


]
