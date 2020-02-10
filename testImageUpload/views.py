from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm

class HomePageView(ListView):
    print("Reached inside the view !!")
    model = Post
    template_name = "image_home.html"

class CreatePostView(CreateView): # new
    model = Post
    form_class = PostForm
    template_name = 'post.html'
    success_url = reverse_lazy('image_home')

# def create_post_view_functionview_version(request): 
#     if request.method == 'POST': 
#         form = PostForm(request.POST, request.FILES) 
#         if form.is_valid(): 
#             form.save() 
#             return redirect('success') 
#     else: 
#         form = PostForm() 
#     return render(request, 'hotel_image_form.html', {'form' : form}) 
  