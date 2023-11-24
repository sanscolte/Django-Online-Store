from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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
        reviews_context = Review.objects.filter(product__pk=pk)
        product_context = Product.objects.get(pk=pk)

        print(reviews_context, product_context)

        response = self.client.get(reverse("products:product-detail", args=(pk,)))

        self.assertEqual(response.status_code, 200)

        # FIXME перед ассертами отпринтуй response.context и response.json(), чтобы понимать что с чем сравнивать
        self.assertEqual(response.context["reviews"], reviews_context)
        self.assertEqual(response.context["product"], product_context)

    def test_view_post(self):
        """Тестирование отправки POST-запроса"""

        pk: int = 1
        form = {
            "text": "test review",
            "rating": 5,
        }

        response = self.client.post(reverse("products:product-detail", args=(pk,)), data=form)

        self.assertRedirects(response, reverse("products:product-detail", args=(pk,)))

        # FIXME перед ассертом отпринтуй response.context и response.json(), чтобы понимать что с чем сравнивать
        self.assertEqual(response.context["success"], True)
