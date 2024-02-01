from typing import Union

from django import forms
from django.core.exceptions import ValidationError

from payment.utils import card_number_is_valid


class PaymentForm(forms.Form):
    """Форма ввода номера карты"""

    card_number = forms.CharField(
        min_length=9,
        max_length=9,
        widget=forms.TextInput(
            attrs={
                "class": "form-input Payment-bill",
                "placeholder": "9999 9999",
                "data-mask": "9999 9999",
            }
        ),
    )

    def clean_card_number(self) -> Union[str, ValidationError]:
        """
        Проверяет номер карты на валидность
        :return: Union[str, ValidationError]
        :raises: ValidationError
        """
        data: str = self.cleaned_data["card_number"]
        if not card_number_is_valid(data):
            raise ValidationError("Номер карты должен быть 8-значным четным числом, не заканчивающимся на 0")
        return data
