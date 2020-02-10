from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # path('', views.test_page, name='test_page'),
    path('', views.landing_page, name='landing_page'),
    path('bootstrap/', TemplateView.as_view(template_name="bootstrap/test_bootstrap.html")),
]
