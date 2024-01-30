from orders.models import Order, Status
from payment.models import BankTransaction
from payment.utils import card_number_is_valid


class PaymentService:
    """Сервис оплаты заказа"""

    def __init__(self, order: Order, card_number, total_price, transaction: BankTransaction):
        self.order = order
        self.card_number = str(card_number)
        self.total_price = total_price

    def pay(self):
        if card_number_is_valid(self.card_number):
            self.order.status = Status.STATUS_PAID
            self.order.save()
            # transaction.is_success = True
            # transaction.save()

            # TODO сделать уменьшение остатков в модели Offer

            return f"Оплата заказа №{self.order_id} с карты {self.card_number} на сумму ${self.total_price}"
        else:
            self.order.status = Status.STATUS_NOT_PAID
            self.order.save()
            # transaction.is_success = False
            # transaction.save()
            return (
                f"Не удалось оплатить заказ №{self.order_id} с карты {self.card_number} на сумму ${self.total_price}."
                f"Причина: номер карты невалидный"
            )
