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

        if not json_file.name.endswith(".json"):
            raise forms.ValidationError("Файл должен быть в формате JSON")
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("Наименование обязательно для заполнения")
        return name

    def clean_category(self):
        category = self.cleaned_data.get("category")
        if not category:
            raise forms.ValidationError("Категория обязательна для заполнения")
        return category
