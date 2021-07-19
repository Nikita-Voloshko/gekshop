
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)

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
