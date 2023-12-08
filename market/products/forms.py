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
