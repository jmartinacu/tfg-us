from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is None:
                # TODO: add error message
                return render(request, "users/login.html", {"form": form})
            login(request, user)
            return redirect(reverse("home:home_images"))
        else:
            return render(request, "users/login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home:home_images"))
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("home:home_images"))
