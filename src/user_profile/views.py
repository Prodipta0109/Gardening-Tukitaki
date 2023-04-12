from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .forms import(
    UserRegistrationForm,
    LoginForm
)


# Create your views here.
@never_cache
def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "Wrong credentials")

    context = {
        "form": form
    }
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')

@never_cache
def register_user(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, "Registration sucessful")
            return redirect('login')

    context = {
        "form": form
    }
    return render(request, 'registration.html', context)

