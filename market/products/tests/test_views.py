from django.test import TestCase
from django.urls import reverse

from products.models import Product


class TestProductListView(TestCase):
    """Класс тестов представлений продуктов"""

    fixtures = ["04-shops.json", "05-categories.json", "06-products.json", "08-offers.json"]

    def test_filter(self):
        """Проверка наличия продукта на странице"""

        url = reverse("products:product-list") + "?name=Smeg"
        response = self.client.get(url)
        product_count = Product.objects.filter(name="Smeg").count()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smeg")
        self.assertEqual(product_count, 1)

    def test_price(self):
        """Проверка цены на понижение"""
        url = reverse("products:product-list")
        response = self.client.get(url)
        products = response.context_data["object_list"]
        price = 0
        for product in products:
            if price >= product.min_price[0]:
                raise ValueError
            else:
                price = product.min_price[0]
