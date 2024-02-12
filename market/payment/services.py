from decimal import Decimal

from orders.models import Order, Status, OrderItem
from payment.models import BankTransaction
from payment.utils import card_number_is_valid


class PaymentService:
    """
    Сервис оплаты заказа

    Args:
        order (Order): экземпляр заказа
        card_number (str): номер карты
        total_price (Decimal): общая стоимость заказа
        transaction (BankTransaction): экземпляр BankTransaction, с которым работаем
    """

    def __init__(self, order: Order, card_number: str, total_price: Decimal, transaction: BankTransaction):
        self.order = order
        self.card_number = str(card_number)
        self.total_price = total_price
        self.transaction = transaction

    def pay(self) -> str:
        """
        Метод оплаты заказа, проверяет валидность номера карты,
        ставит соответствующий статус заказа,
        статус в модели оплаты и уменьшает остатки продуктов на складе
        :return: str
        """
        if card_number_is_valid(self.card_number):
            self.order.status = Status.STATUS_PAID
            self.order.save()
            self.transaction.is_success = True
            self.transaction.save()

            for item in OrderItem.objects.filter(order=self.order):
                item.offer.remains -= item.quantity
                item.offer.save()

            return f"Оплата заказа №{self.order.id} с карты {self.card_number} на сумму ${self.total_price}"

        else:
            self.order.status = Status.STATUS_NOT_PAID
            self.order.save()
            self.transaction.is_success = False
            self.transaction.save()
            return (
                f"Не удалось оплатить заказ №{self.order.id} с карты {self.card_number} на сумму ${self.total_price}. "
                f"Причина: номер карты невалидный"
            )
