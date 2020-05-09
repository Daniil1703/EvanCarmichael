from django import forms
from django.contrib.auth.forms import PasswordChangeForm,\
    UserCreationForm, UserChangeForm,PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import CustomUser, Profile

class CaptchaForm(forms.Form):
    captcha = CaptchaField(
        label=(''),
        # widget=CustomCaptchaTextInput(attrs={'class':'form-control'})
    )
    class Meta:
        fields = ['captcha']


class CustomUserCreationForm(UserCreationForm):
    login_user = forms.CharField(
        label=('Логин:'),
        widget=forms.TextInput(attrs={'class': 'un'}),
    )
    email = forms.EmailField(
        label=('Email:'),
        widget=forms.EmailInput(attrs={'class': 'un'}),
    )
    password1 = forms.CharField(
        label=('Пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )
    password2 = forms.CharField(
        label=('Повторите пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )
    captcha = CaptchaField(
        label=('')
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = [
            'login_user', 'email'
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        rs = CustomUser.objects.filter(email=email)
        if rs.count():
            raise ValidationError("Такой email уже зарегистрирован!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

class LoginForm(forms.Form):
    email = forms.EmailField(
        label=('Email:'),
        widget=forms.EmailInput(attrs={'class': 'un'}),
    )

    password = forms.CharField(
        label=('Пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )

    class Meta(object):
        model = CustomUser

        fields = [
            'email', 'password'
        ]

class SecureLoginForm(forms.Form):
    email = forms.EmailField(
        label=('Email:'),
        widget=forms.EmailInput(attrs={'class': 'un'}),
    )

    password = forms.CharField(
        label=('Пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )
    captcha = CaptchaField(
        label=(''),
    )

    class Meta(object):
        model = CustomUser

        fields = [
            'email', 'password', 'captcha'
        ]

class PassChForm(PasswordChangeForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
        'password_incorrect': "Неверный старый пароль. "
                                "Попробуйте еще раз.",
    }

    old_password = forms.CharField(
        label=('Старый пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )
    new_password1 = forms.CharField(
        label=('Новый пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )
    new_password2 = forms.CharField(
        label=('Повторите пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )

# Наследуемся от стандартного сброса пароля и делаем свое поле для mail
class PassResForm(PasswordResetForm):
    email = forms.EmailField(
        label=('Email указанный при регистрации:'),
        widget=forms.EmailInput(attrs={'class': 'un'}),
    )
    captcha = CaptchaField(
        label=('')
    )


class SetPassForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают",
    }
    new_password1 = forms.CharField(
        label=('Новый пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )
    new_password2 = forms.CharField(
        label=('Повторите пароль:'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'pass'}),
    )


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        label=('Email:'),
        widget=forms.EmailInput(attrs={'class': 'un'}),
    )

    class Meta:
        model = CustomUser
        fields = ['email']

class ProfileUpdateFrom(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'upload-image',
                                      'id': 'upload-image'}),
    )
    class Meta:
        model = Profile
        fields = ['picture']
