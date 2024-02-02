from django.test import TestCase
from orders.models import Order


class OrderFixturesTest(TestCase):
    """Класс тестов фикстур модели Order"""

    fixtures = ["fixtures/23-orders.json"]

    def test_fixtures_len(self):
        self.assertEqual(Order.objects.count(), 10)
