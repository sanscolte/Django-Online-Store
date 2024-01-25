from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Менеджер модели пользователя, где адрес электронной почты является уникальным идентификатором.
    для аутентификации вместо имен пользователей.
    """

    def create_user(self, email: str, password: str, **extra_fields: dict) -> str:
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError("Адрес электронной почты должен быть установлен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: dict):
        """
        Создает и сохраняет администратора с указанным адресом электронной почты и паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Администратор должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Администратор должен иметь is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
