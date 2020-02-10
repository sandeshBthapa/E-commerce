from django.shortcuts import render
from .forms import ContactForm

# Create your views here.
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact",
        "content": "Welcome to the contact page !",
        "form": contact_form,
        # "brand": "New test brand name"
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        context["form"] = ContactForm()
    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get("fullname"))
    return render(request, "contact/view.html", context=context)