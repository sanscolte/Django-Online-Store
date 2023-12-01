from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from products.models import Product
from django.contrib.auth import get_user_model


class TestProductListView(TestCase):
    """Класс тестов представлений продуктов"""

    fixtures = ["04-shops.json", "05-categories.json", "06-products.json", "08-offers.json"]

    def setUp(self) -> None:
        cache.clear()

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
            if price == 0:
                price = product.avg_price
            self.assertTrue(price >= product.avg_price)
            price = product.avg_price


User = get_user_model()


class ProductDetailReviewTest(TestCase):
    """Класс тестов представлений отзывов детальной страницы продукта"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
        "fixtures/16-reviews.json",
    ]

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_view_with_reviews(self):
        """Тестирование контекста с отзывами"""

        pk: int = 1
        response = self.client.get(reverse("products:product-detail", args=[pk]))
        reviews = response.context_data.get("reviews")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("reviews" in response.context_data)
        self.assertEqual(reviews.number, 1)
        self.assertEqual(len(reviews), 3)

    def test_view_without_reviews(self):
        """Тестирование контекста без отзывов"""

        pk: int = 10
        response = self.client.get(reverse("products:product-detail", args=[pk]))
        reviews = response.context_data.get("reviews")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("reviews" in response.context_data)
        self.assertEqual(reviews.number, 1)
        self.assertEqual(len(reviews), 0)

    def test_view_post(self):
        """Тестирование отправки POST-запроса"""

        pk: int = 1
        review_form: dict[str, int] = {
            "text": "test review",
            "rating": 5,
        }
        response = self.client.post(reverse("products:product-detail", args=(pk,)), data=review_form)

        self.assertRedirects(response, reverse("products:product-detail", args=(pk,)))
