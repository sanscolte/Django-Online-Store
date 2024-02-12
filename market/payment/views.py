from decimal import Decimal, ROUND_DOWN
from typing import Union, Dict

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.viewsets import ModelViewSet

from payment.forms import PaymentForm
from payment.models import BankTransaction
from payment.serializers import BankTransactionSerializer
from cart.services import CartServices


class BankTransactionViewSet(ModelViewSet):
    """API для создания модели оплаты"""

    queryset = BankTransaction.objects.all()
    serializer_class = BankTransactionSerializer


class PaymentWithCardView(TemplateView):
    """Представление оплаты заказа с карты"""

    template_name = "payment/payment_with_card.jinja2"

    def post(self, request, *args, **kwargs):
        form: PaymentForm = PaymentForm(self.request.POST)
        if form.is_valid():
            order: int = request.GET.get("order")
            card_number: str = form.cleaned_data["card_number"]
            total_price: Decimal = Decimal(request.GET.get("total_price"))
            rounded_total_price: Decimal = total_price.quantize(Decimal("0.00"), rounding=ROUND_DOWN)
            cart = CartServices(request)

            data: Dict[str, Union[str, int, Decimal]] = {
                "order": order,
                "card_number": card_number,
                "total_price": rounded_total_price,
            }

            serializer: BankTransactionSerializer = BankTransactionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                cart.clear()
            else:
                print(serializer.errors)

            return HttpResponseRedirect(reverse("payment:progress_payment"))
        return render(
            request=self.request,
            template_name="payment/payment_with_card.jinja2",
            context={"form": form},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PaymentForm()
        return context


class ProgressPaymentView(TemplateView):
    """Представление прогресса оплаты заказа"""

    template_name = "payment/progress_payment.jinja2"
