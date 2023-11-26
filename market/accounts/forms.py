from django.contrib.auth.forms import AuthenticationForm
from django import forms


class UserLoginForm(AuthenticationForm):
    """Класс отвечает за аутентификацию пользователя"""

    username = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "data-validate": "require",
                "placeholder": "Введите e-mail",
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "data-validate": "require",
                "placeholder": "Введите пароль",
                "autocomplete": "password",
            }
        ),
    )
