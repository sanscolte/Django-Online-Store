from django import forms


class PaymentForm(forms.Form):
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

    def clean(self):
        # card_number = self.cleaned_data.get('card_number')
        ...
