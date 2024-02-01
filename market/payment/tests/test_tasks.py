from decimal import Decimal
from django.test import TestCase

from orders.models import Status, Order
from payment.models import BankTransaction
from payment.services import PaymentService

success_response: str = "Оплата заказа №5 с карты 4444 4444 на сумму $100.00"
failed_response: str = (
    "Не удалось оплатить заказ №5 с карты 0000 0000 на сумму $100.00. " "Причина: номер карты невалидный"
)


class PaymentServiceTestCase(TestCase):
    """Класс тестов для сервиса оплаты"""

    fixtures = ["23-orders.json"]

    def setUp(self):
        self.order: Order = Order.objects.get(pk=5)
        self.transaction: BankTransaction = BankTransaction.objects.create(
            order=self.order, card_number="2222 2222", total_price=100.00
        )

    def test_successful_payment(self):
        """Тест успешной оплаты"""
        service: PaymentService = PaymentService(self.order, "4444 4444", Decimal("100.00"), self.transaction)
        result: str = service.pay()

        self.assertEqual(result, success_response)
        self.assertEqual(self.order.status, Status.STATUS_PAID)
        self.assertTrue(self.transaction.is_success)

    def test_failed_payment(self):
        """Тест неуспешной оплаты"""
        service: PaymentService = PaymentService(self.order, "0000 0000", Decimal("100.00"), self.transaction)
        result: str = service.pay()

        self.assertEqual(result, failed_response)
        self.assertEqual(self.order.status, Status.STATUS_NOT_PAID)
        self.assertFalse(self.transaction.is_success)
