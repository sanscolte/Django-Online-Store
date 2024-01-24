from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from orders.models import Order
from payment.mixins import PaymentMixin
from payment.tasks import pay


class PaymentWithCardView(PaymentMixin, TemplateView):
    """Отображение шаблона оплаты заказа с карты"""

    template_name = "payment/payment_with_card.jinja2"


class ProgressPaymentView(TemplateView):
    template_name = "payment/progress_payment.jinja2"

    def get(self, request, *args, **kwargs):
        order_id = request.session.get("order_id")
        order = Order.objects.get(id=order_id)
        card_number = request.session.get("card_number")
        message = pay.delay(order.pk, card_number, order.total_price)
        request.session["payment_message"] = message.info
        del request.session["card_number"]
        del request.session["order_id"]
        return HttpResponseRedirect(reverse("product:catalog"))
