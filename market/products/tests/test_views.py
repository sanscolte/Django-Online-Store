from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from products.models import Product


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
        cache.clear()

    def test_view_with_reviews(self):
        """Тестирование контекста с отзывами"""

        pk: int = 1
        response = self.client.get(reverse("products:product-detail", args=[pk]))
        reviews = response.context_data.get("reviews")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отзывы")
        self.assertEqual(reviews.number, 1)
        self.assertEqual(len(reviews), 3)

    def test_view_without_reviews(self):
        """Тестирование контекста без отзывов"""

        pk: int = 10
        response = self.client.get(reverse("products:product-detail", args=[pk]))
        reviews = response.context_data.get("reviews")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отзывы")
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


class ProductDetailTest(TestCase):
    """Класс тестов представлений детальной страницы продукта"""

    fixtures = [
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
    ]

    def test_view_product_detail_page(self):
        """Тестирование представления страницы с деталями продукта"""

        pk = 1
        response = self.client.get(reverse("products:product-detail", args=[pk]))
        product = Product.objects.get(pk=pk)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product)
