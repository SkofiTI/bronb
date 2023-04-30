from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, UserLoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile_url')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile_url')
    else:
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                phone_number = request.POST["phone_number"]
                password = request.POST["password"]
                user = authenticate(request, phone_number=phone_number, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile_url', permanent=True)
                else:
                    form.add_error(None, 'Invalid phone number or password')
        else:
            form = UserLoginForm()
    return render(request, 'authentication/login.html', {'form': form})


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect('rooms_list_url')
