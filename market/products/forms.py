from django import forms

from .models import Review


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
