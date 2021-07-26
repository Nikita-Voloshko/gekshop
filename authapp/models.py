
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from datetime import datetime

now = datetime.now()



class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', blank=True, null=True)
    email = models.EmailField(('email address'), unique=False)
    is_delet = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now + timedelta(hours=48)))

    def is_activation_key_expires(self):
        if now <= self.activation_key_expires:
           return False

        return True




'''from django.contrib.auth.models import AbstractUser
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    age = models.PositiveSmallIntegerField(default=0)
    first_name = models.CharField(max_length=30, default='Введите имя пользователя')
    last_name = models.CharField(max_length=150, default='Введите фамилию пользователя')
    username = models.CharField(unique=True, max_length=64)
    email = models.EmailField(blank=True, max_length=254, verbose_name='email address', null=True)'''
