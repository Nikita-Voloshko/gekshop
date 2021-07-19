
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from authapp.forms import loginUser, registerUser, ChangeProfil
from basket.views import Basket


# Create your views here.


def login(request):
    if request.method == "POST":
        form = loginUser(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = loginUser()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == "POST":
        form = registerUser(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = registerUser()
    context = {'form': form}
    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request):
    if request.method == 'POST':
        form = ChangeProfil(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('auth:profil'))
    else:
        form = ChangeProfil(instance=request.user)
    context = {
                'form': form,
                'baskets': Basket.objects.filter(user=request.user),
            }
    return render(request, 'authapp/profile.html', context)
