from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from authapp.models import User, UserProfile
import random, hashlib


class loginUser(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(loginUser, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class registerUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(registerUser, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self):
        user = super(registerUser, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode(encoding='UTF-8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(str(user.email + salt).encode(encoding='UTF-8')).hexdigest()[:6]
        user.save()
        return user



class ChangeProfil(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super(ChangeProfil, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'
        self.fields['first_name'].widget.attrs['readonly'] = False
        self.fields['last_name'].widget.attrs['readonly'] = False


class ProfileChangeProfil(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'about_me', 'chosegender')

    def __init__(self, *args, **kwargs):
        super(ProfileChangeProfil, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'