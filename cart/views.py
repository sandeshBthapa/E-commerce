from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart
from orders.models import Order
from billing.models import BillingProfile
from loginRegister.forms import LoginForm, GuestForm
from loginRegister.models import GuestEmail

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    print(request.session)
    # print(dir(request.session))
    # request.session.set_expiry(300) # 5 minuts by default
    # print(request.session.session_key)
    return render(request, "cart/view.html", {"cart":cart_obj,"isNew":new_obj})

def cart_update(request):
    if request.is_ajax:
        print("An Ajax request")
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        if product_id is not None:
            try:
                product_obj = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                print("There is no product with id : ", product_id)
                return redirect("cart:home")
            cart_obj, new_obj = Cart.objects.new_or_get(request)
            # return redirect(product_obj.get_absolute_url())
            if product_obj in cart_obj.products.all():
                cart_obj.products.remove(product_obj)
            else:
                cart_obj.products.add(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_emai_id = request.session.get("guest_email_id")
    user = request.user
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_emai_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_emai_id)
        billing_profile, billing_guest_profile_created = BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass
    context = {
        "order":order_obj,
        "billing_profile":billing_profile,
        "login_form":login_form,
        "guest_form":guest_form
    }
    return render(request, "cart/checkout.html", context)



 