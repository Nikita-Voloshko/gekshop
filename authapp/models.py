from django.db.models import Model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from datetime import timedelta
from datetime import datetime
from django.db.models.signals import post_save

now = datetime.now()



class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', blank=True, null=True)
    email = models.EmailField(verbose_name='email address', unique=False, blank=True, null=True)
    is_delet = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, blank=True)
'''    activation_key_expires = models.DateTimeField(default=(now + timedelta(hours=48)))

    def is_activation_key_expires(self):
        if now <= self.activation_key_expires:
            return False

        return True'''


class UserProfile(Model):
    Male = 'М'
    FEMALE = 'Ж'

    ChoseGender = ((Male, 'М'), (FEMALE, 'Ж'))
    user = models.OneToOneField(
        User,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )

    tagline = models.CharField(
        verbose_name='теги',
        max_length=128,
        blank=True
    )

    about_me = models.CharField(
        verbose_name='О себе',
        max_length=512,
        blank=True
    )

    chosegender = models.CharField(
        verbose_name='имя',
        max_length=1,
        choices=ChoseGender,
        blank=True
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance,created, **kwargs):
        if created:
            UserProfile.objects.created(user=instance)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, **kwargs):
        instance.UserProfile.save()


