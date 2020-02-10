from django.shortcuts import render
from products.models import Product

# Create your views here.
def landing_page(request):
    product_list = Product.objects.all()
    context = {
        "title":            "Landing Page.",
        "content":          "Welcome to the landing page.",
        "product_list":     product_list,
        # "premium_content":  "Some premium content"
    }
    if request.user.is_authenticated:
        context['premium_content'] = "This is for subscribed users only !!"
    return render(request, 'landing_page.html', context)
    
def test_page(request):
    context = {
        "title":    "Testing",
        "content":  "Testing in action.",
    }
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get("fullname"))
        
    if request.user.is_authenticated:
        context['premium_content'] = "This is for subscribed users only !!"
    return render(request, 'testFiles/form_example.html', context)