import random
from typing import Union

from django.core.exceptions import ObjectDoesNotExist

from orders.models import Order, Status
from payment.utils import card_number_is_valid


class PaymentService:
    """Сервис оплаты заказа"""

    def __init__(self, order_id, card_number, total_price):
        self.order_id = order_id
        self.card_number = str(card_number)
        self.total_price = total_price

    def pay(self):
        order = self._get_order()

        if card_number_is_valid(self.card_number):
            order.status = self._get_random_success_status()
            order.save()
            return f"Оплата заказа №{self.order_id} с карты {self.card_number} на сумму ${self.total_price}"
        else:
            order.status = Status.STATUS_NOT_PAID
            order.save()
            return (
                f"Не удалось оплатить заказ №{self.order_id} с карты {self.card_number} на сумму ${self.total_price}."
                f"Причина: ..."
            )

    def _get_order(self) -> Union[Order, str]:
        """
        Получает заказ, который нужно оплатить, или в случае неудачи, возвращает сообщение об ошибке
        :return: заказ или сообщение об ошибке
        """
        try:
            return Order.objects.get(id=self.order_id)
        except ObjectDoesNotExist:
            return f"Заказа не существует"  # noqa

    def _get_random_success_status(self) -> str:
        """
        Получает случайный успешный статус
        :return:
        """
        return random.choice([Status.STATUS_OK, Status.STATUS_DELIVERED, Status.STATUS_PAID])
