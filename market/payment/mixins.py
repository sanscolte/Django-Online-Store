from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from payment.forms import PaymentForm


class PaymentMixin(FormMixin):
    """Миксин для отправки POST-запроса оплаты заказа"""

    form_class = PaymentForm
    http_method_names = ["get", "post"]

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            self.request.session["card_number"] = form.cleaned_data["card_number"]
            return HttpResponseRedirect(reverse("payment:progress_payment"))
        return render(
            request=self.request,
            template_name="payment/payment_with_card.jinja2",
            context={"form": form},
        )
