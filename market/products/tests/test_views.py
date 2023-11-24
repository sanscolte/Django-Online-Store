from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core import serializers

from products.models import Review, Product

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

    def test_view_context(self):
        """Тестирование передачи данных в контексте"""

        pk: int = 1
        reviews_context = serializers.serialize("json", Review.objects.filter(product__pk=pk))
        product_context = Product.objects.get(pk=pk)

        response_reviews_context = serializers.serialize(
            "json", self.client.get(reverse("products:product-detail", args=(pk,))).context_data["reviews"]
        )
        response_product_context = self.client.get(reverse("products:product-detail", args=(pk,))).context_data[
            "product"
        ]

        self.assertEqual(response_reviews_context, reviews_context)
        self.assertEqual(response_product_context, product_context)

    def test_view_post(self):
        """Тестирование отправки POST-запроса"""

        pk: int = 1
        review_form: dict[str, int] = {
            "text": "test review",
            "rating": 5,
        }
        response = self.client.post(reverse("products:product-detail", args=(pk,)), data=review_form)

        self.assertRedirects(response, reverse("products:product-detail", args=(pk,)))
