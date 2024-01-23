from django import forms

from .models import Review, ProductDetail, ProductImage


class ReviewForm(forms.ModelForm):
    # TODO добавить докстринг
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
    # TODO добавить докстринг
    class Meta:
        model = ProductDetail
        fields = "detail", "value"


class ProductImageForm(forms.ModelForm):
    # TODO добавить докстринг
    class Meta:
        model = ProductImage
        fields = "image", "sort_image"


class MultipleFileInput(forms.ClearableFileInput):
    # TODO добавить докстринг
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    # TODO добавить докстринг
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
    # TODO добавить докстринг
    email = forms.EmailField(label="Email для обратной связи", required=False)
    json_files = MultipleFileField(label="Файлы для импорта", required=True)
