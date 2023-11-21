from django.test import TestCase
from django.urls import reverse

from shops.models import Shop


class ShopDetailViewTest(TestCase):
    """Класс тестов представлений деталей магазина"""

    fixtures = [
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
        "fixtures/08-offers.json",
    ]

    def test_shop_detail(self):
        pk = 35
        response = self.client.get(reverse("shops:shops_detail", args=[pk]))
        shop = Shop.objects.get(pk=pk)
        self.assertContains(response, shop.name)
