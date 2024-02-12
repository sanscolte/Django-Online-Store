from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .utils import user_preview_directory_path


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    email = models.EmailField(unique=True, verbose_name=_("Email адрес"))
    full_name = models.CharField(max_length=254, verbose_name=_("Полное имя"))
    avatar = models.ImageField(upload_to=user_preview_directory_path, blank=True, verbose_name=_("Аватар"))
    phone_number = models.CharField(max_length=12, unique=True, verbose_name=_("Телефон"))

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_("Дата регистрации"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
