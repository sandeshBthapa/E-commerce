from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('contact/', views.contact_page, name='contact'),
]
