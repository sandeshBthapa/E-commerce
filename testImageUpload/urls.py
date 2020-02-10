from django.urls import path, include
from .views import HomePageView, CreatePostView 

urlpatterns = [
    path("", HomePageView.as_view(), name='image_home' ),
    path('post/', CreatePostView.as_view(), name='add_post')

]
