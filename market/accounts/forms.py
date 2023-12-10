from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import User
from django import forms
from django.utils.translation import gettext_lazy as _


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


class MyUserCreationForm(UserCreationForm):
    """Класс отвечает за форму регистрации пользователя"""

    password1 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "data-validate": "requirePassword",
                "placeholder": "Введите пароль",
                "autocomplete": "new-password",
                "maxlength": "150",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "data-validate": "requireRepeatPassword",
                "placeholder": "Введите пароль повторно",
                "autocomplete": "new-password",
                "maxlength": "150",
            }
        ),
    )
    full_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-input", "data-validate": "require", "placeholder": "Введите ФИО", "maxlength": "254"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        label="e-mail",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "data-validate": "requireMail",
                "placeholder": "Введите E-mail",
                "maxlength": "254",
            }
        ),
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "data-validate": "requirePhone",
                "placeholder": "Введите номер телефона",
                "type": "tel",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("password1", "password2", "full_name", "email", "phone_number")


class MyUserChangeForm(UserChangeForm):
    """Класс отвечает за форму изменения пользователя"""

    error_messages = {
        "password_mismatch": _("The two password fields didn't match."),
    }

    password1 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "data-validate": "requirePassword",
                "placeholder": "Тут можно изменить пароль",
                "autocomplete": "new-password",
                "maxlength": "150",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "data-validate": "requireRepeatPassword",
                "placeholder": "Введите пароль повторно",
                "autocomplete": "new-password",
                "maxlength": "150",
            }
        ),
    )
    full_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-input", "data-validate": "require", "placeholder": "Введите ФИО", "maxlength": "254"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        label="e-mail",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "data-validate": "requireMail",
                "placeholder": "Введите E-mail",
                "maxlength": "254",
            }
        ),
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "data-validate": "requirePhone",
                "placeholder": "Введите номер телефона",
                "type": "tel",
            }
        ),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "Profile-file form-input",
                "type": "file",
                "accept": ".jpg,.gif,.png",
                "data-validate": "onlyImgAvatar",
            }
        ),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("password1", "password2", "full_name", "email", "phone_number", "avatar")


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-input", "data-validate": "require", "maxlength": "254", "autocomplete": "email"}
        ),
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "data-validate": "requirePassword",
                "placeholder": "Введите пароль",
                "autocomplete": "new-password",
                "maxlength": "150",
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        max_length=150,
        required=True,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "data-validate": "requireRepeatPassword",
                "placeholder": "Введите пароль повторно",
                "autocomplete": "new-password",
                "maxlength": "150",
            }
        ),
    )
