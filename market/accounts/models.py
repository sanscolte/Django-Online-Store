from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from .utils import user_preview_directory_path


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email адрес")
    full_name = models.CharField(max_length=254, verbose_name="Полное имя")
    avatar = models.ImageField(upload_to=user_preview_directory_path, blank=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=12, unique=True, verbose_name="Телефон")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
