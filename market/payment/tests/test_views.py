from typing import Dict, Union

from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient

from orders.models import Order
from payment.models import BankTransaction


class BankTransactionAPITest(TestCase):
    """Класс тестов для API оплаты заказа"""

    fixtures = [
        "23-orders.json",
    ]

    def setUp(self):
        self.client = APIClient()
        self.order: Order = Order.objects.get(pk=5)
        self.new_order: Order = Order.objects.get(pk=6)

    def test_post_bank_transaction(self):
        """Тест создания нового экземпляра модели оплаты заказа"""
        url: str = "/ru/payment/api/banktransactions/"
        data: Dict[str, Union[int, str, float]] = {
            "order": self.order.pk,
            "card_number": "1111 1111",
            "total_price": 100.00,
        }
        response: Response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BankTransaction.objects.count(), 1)
        self.assertEqual(BankTransaction.objects.get().order, self.order)
        self.assertEqual(BankTransaction.objects.get().card_number, "1111 1111")
        self.assertEqual(BankTransaction.objects.get().total_price, 100.00)

    def test_get_bank_transaction_list(self):
        """Тест получения экземпляра"""
        BankTransaction.objects.create(order=self.order, card_number="2222 2222", total_price=100.00)
        BankTransaction.objects.create(order=self.new_order, card_number="3333 3333", total_price=200.00)

        url: str = "/ru/payment/api/banktransactions/"
        response: Response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_bank_transaction_detail(self):
        """Тест получения деталей экземпляра"""
        bank_transaction: BankTransaction = BankTransaction.objects.create(
            order=self.order, card_number="4444 4444", total_price=500.00
        )

        url: str = f"/ru/payment/api/banktransactions/{bank_transaction.id}/"
        response: Response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["order"], self.order.pk)
        self.assertEqual(response.data["card_number"], "4444 4444")
        self.assertEqual(response.data["total_price"], "500.00")

    def test_update_bank_transaction(self):
        """Тест частичного изменения экземпляра"""
        bank_transaction: BankTransaction = BankTransaction.objects.create(
            order=self.order, card_number="5555 5555", total_price=100.00
        )

        url: str = f"/ru/payment/api/banktransactions/{bank_transaction.id}/"
        data: Dict[str, Union[int, str, float]] = {
            "order": self.new_order.pk,
            "card_number": "5555 5555",
            "total_price": 200.00,
        }
        response: Response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BankTransaction.objects.get().order, self.new_order)
        self.assertEqual(BankTransaction.objects.get().card_number, "5555 5555")
        self.assertEqual(BankTransaction.objects.get().total_price, 200.00)

    def test_delete_bank_transaction(self):
        """Тест удаления экземпляра"""
        bank_transaction: BankTransaction = BankTransaction.objects.create(
            order=self.order, card_number="6666 6666", total_price=100.00
        )

        url: str = f"/ru/payment/api/banktransactions/{bank_transaction.id}/"
        response: Response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(BankTransaction.objects.count(), 0)
