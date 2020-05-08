from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login_user = models.CharField(
        _('Логин'), unique=True, db_index=True, max_length=40
    )
    email = models.EmailField(_('email адресс'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('пользователя')
        verbose_name_plural = _('пользователи')

    def __str__(self):
         return self.email

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    picture = models.ImageField(_('Фотография'), default='user_pics/default_pic.png',
                                upload_to='user_pics/%Y/')

    class Meta:
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')

    def __str__(self):
        return f'Аккаунт {self.user.login_user}'
