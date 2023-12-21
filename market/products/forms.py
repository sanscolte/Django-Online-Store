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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductImportForm(forms.Form):
    email = forms.EmailField(label="Email для обратной связи")
    json_files = MultipleFileField(label="Файлы для импорта")

    def clean(self):  # noqa
        cleaned_data = super().clean()
        json_files = cleaned_data.get("json_files")

        try:
            json_data = [json.load(json_file) for json_file in json_files][0]
        except json.decoder.JSONDecodeError:
            raise forms.ValidationError("Ошибка при чтении файла JSON")

        for json_file in json_files:
            if not json_file.name.endswith(".json"):
                raise forms.ValidationError("Файл должен быть в формате JSON")

        for json_object in json_data:
            try:
                json_object["Товар"]
            except KeyError:
                raise forms.ValidationError("Наименование товара обязательно для заполнения")
            try:
                json_object["Категория товара"]
            except KeyError:
                raise forms.ValidationError("Категория товара обязательна для заполнения")
            try:
                json_object["Магазин"]
            except KeyError:
                raise forms.ValidationError("Наименование магазина обязательно для заполнения")
            try:
                json_object["Телефон"]
            except KeyError:
                raise forms.ValidationError("Телефон магазина обязателен для заполнения")
            try:
                json_object["Адрес"]
            except KeyError:
                raise forms.ValidationError("Адрес магазина обязателен для заполнения")
            try:
                json_object["Email"]
            except KeyError:
                raise forms.ValidationError("Email магазина обязателен для заполнения")
            try:
                json_object["Магазин оффера"]
            except KeyError:
                raise forms.ValidationError("Магазин оффера обязателен для заполнения")
            try:
                json_object["Продукт оффера"]
            except KeyError:
                raise forms.ValidationError("Продукт оффера обязателен для заполнения")
            try:
                json_object["Цена оффера"]
            except KeyError:
                raise forms.ValidationError("Цена оффера обязательна для заполнения")
            try:
                json_object["Остатки"]
            except KeyError:
                raise forms.ValidationError("Остатки товара обязательны для заполнения")

        return cleaned_data
