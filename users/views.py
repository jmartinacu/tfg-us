from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SigninForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Usuario no encontrado")
                return render(request, "users/login.html", {"form": form})
            login(request, user)
            return redirect(reverse("home:home_images"))
        else:
            return render(request, "users/login.html", {"form": form})
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home:home_images"))
    else:
        form = SigninForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("home:home_images"))
