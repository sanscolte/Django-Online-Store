import json

from django import forms

from .models import Review, ProductDetail, ProductImage


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("text",)

        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "name": "review",
                    "id": "review",
                    "placeholder": "Отзыв",
                },
            ),
        }


class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "detail", "value"


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = "image", "sort_image"


class ProductImportForm(forms.Form):
    json_file = forms.FileField()

    def clean(self):
        cleaned_data = super().clean()
        json_file = cleaned_data.get("json_file")
        json_data = json.load(json_file)[0]

        if not json_file.name.endswith(".json"):
            raise forms.ValidationError("Файл должен быть в формате JSON")
        try:
            name = json_data["fields"]["name"]  # noqa
        except KeyError:
            raise forms.ValidationError("Наименование обязательно для заполнения")

        try:
            category = json_data["fields"]["category"]  # noqa
        except KeyError:
            raise forms.ValidationError("Категория обязательна для заполнения")

        return cleaned_data
