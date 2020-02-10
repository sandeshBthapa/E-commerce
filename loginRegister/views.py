from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

User = get_user_model()
# Create your views here.
def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {
        "form":login_form,
    }
    # print("User logged in status : ", end='')
    # print(request.user.is_authenticated)
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if login_form.is_valid():
        print(login_form.cleaned_data)
        # context['form'] = LoginForm()
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        print("Authenticated user is : ",user)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            print(request.user.is_authenticated)
            print("Yay ! user successfully logged in !!")
            # context['form'] = LoginForm()
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("Error while loggin in !!")
    return render(request, 'auth/login.html', context)
    

def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {
        "form":register_form,
    }  
    if register_form.is_valid():
        print(register_form.cleaned_data)
        username = register_form.cleaned_data['username']
        email = register_form.cleaned_data['email']        
        password = register_form.cleaned_data['password']

        new_user = User.objects.create_user(username,email,password)
        authenticate(request, username = new_user.username, password = new_user.password)
        login(request, new_user)

        return redirect('/')
    return render(request, 'auth/register.html', context)

def logout_and_redirect(request):
    logout(request)
    return redirect('/')

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form":form,
    }
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")

        