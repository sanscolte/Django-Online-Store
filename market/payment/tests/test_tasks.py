from decimal import Decimal
from typing import List

from django.test import TestCase

from orders.models import Status, Order, OrderItem
from payment.models import BankTransaction
from payment.services import PaymentService
from shops.models import Offer

success_response: str = "Оплата заказа №5 с карты 4444 4444 на сумму $100.00"
failed_response: str = (
    "Не удалось оплатить заказ №5 с карты 0000 0000 на сумму $100.00. " "Причина: номер карты невалидный"
)


class PaymentServiceTestCase(TestCase):
    """Класс тестов для сервиса оплаты"""

    fixtures = [
        "04-shops.json",
        "05-categories.json",
        "06-products.json",
        "08-offers.json",
        "23-orders.json",
        "24-orders_item.json",
    ]

    def setUp(self):
        self.order: Order = Order.objects.get(pk=5)
        self.order_item: List[OrderItem] = OrderItem.objects.filter(order=self.order)
        self.transaction: BankTransaction = BankTransaction.objects.create(
            order=self.order, card_number="2222 2222", total_price=100.00
        )

    def test_successful_payment(self):
        """Тест успешной оплаты"""
        before_remains: List[int] = []
        after_remains: List[int] = []

        for item in self.order_item:
            offer: Offer = Offer.objects.get(pk=item.offer.pk)
            before_remains.append(offer.remains)

        service: PaymentService = PaymentService(self.order, "4444 4444", Decimal("100.00"), self.transaction)
        result: str = service.pay()

        self.assertEqual(result, success_response)
        self.assertEqual(self.order.status, Status.STATUS_PAID)
        self.assertTrue(self.transaction.is_success)

        for item in self.order_item:
            offer: Offer = Offer.objects.get(pk=item.offer.pk)
            after_remains.append(offer.remains)

        for before, after in zip(before_remains, after_remains):
            self.assertLess(after, before)

    # def test_failed_payment(self):
    #     """Тест неуспешной оплаты"""
    #     service: PaymentService = PaymentService(self.order, "0000 0000", Decimal("100.00"), self.transaction)
    #     result: str = service.pay()
    #
    #     self.assertEqual(result, failed_response)
    #     self.assertEqual(self.order.status, Status.STATUS_NOT_PAID)
    #     self.assertFalse(self.transaction.is_success)
