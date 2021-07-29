
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages


from authapp.forms import loginUser, registerUser, ChangeProfil, ProfileChangeProfil
from authapp.models import User
from basket.views import Basket
from Geekshop import settings
from django.core.mail import send_mail


# Create your views here.

def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Активация на сайте пользователя - {user.username}'

    message = f'Для активации вашей учетный записи {user.username} на портале {settings.DOMAIN_NAME}перейдите по ссылки: \n {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):
    if request.method == 'POST':
        form = loginUser(data=request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = loginUser()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


def register(request):
    title = 'Регистрация'
    if request.method == "POST":
        form = registerUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_email(user):
                messages.success(request, 'Вы успешно зарегестрировались!')
                messages.success(request, 'Активируйте акаунт через почту!')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                messages.error(request, 'Неудалось отправить письмо!!!')
                return HttpResponseRedirect(reverse('auth:login'))

    else:
        form = registerUser()
    context = {'form': form, 'title':title}
    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def profile(request):
    if request.method == 'POST':
        form = ChangeProfil(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = ProfileChangeProfil(data=request.POST, instance=request.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('auth:profil'))
    else:
        form = ChangeProfil(instance=request.user)
        profile_form = ProfileChangeProfil(instance=request.userprofile)
    context = {
                'form': form,
                'baskets': Basket.objects.filter(user=request.user),
                'profile_form': profile_form,
            }
    return render(request, 'authapp/profile.html', context)

def verify(request, email, activation_key):
    user = User.objects.get(email=email)
    if user.activation_key == activation_key:
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request, 'authapp/verify.html')
    else:
        print(f'Ошибка активации - {user.username}')
        return render(request, 'authapp/login.html')

