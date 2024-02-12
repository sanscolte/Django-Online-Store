from django import forms
from django.forms import TextInput, Textarea, RadioSelect
from .models import Order
from accounts.forms import MyUserCreationForm


class OrderStepOneForm(MyUserCreationForm):
    """
    Форма для обработки первого шага заказа товара
    """

    pass


class OrderStepTwoForm(forms.ModelForm):
    """
    Форма для обработки второго шага заказа товара
    """

    class Meta:
        model = Order
        fields = (
            "delivery_type",
            "city",
            "address",
        )
        widgets = {
            "city": TextInput(attrs={"class": "form-input"}),
            "address": Textarea(attrs={"class": "form-textarea"}),
            "delivery_type": RadioSelect,
        }


class OrderStepThreeForm(forms.ModelForm):
    """
    Форма для обработки третьего заказа товара
    """

    class Meta:
        model = Order
        fields = ("payment_type",)
        widgets = {
            "payment_type": RadioSelect,
        }
