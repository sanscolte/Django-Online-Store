from django import forms

from .models import Review, ProductDetail, ProductImage


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "text", "rating"


class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = "detail", "value"


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = "image", "sort_image"
