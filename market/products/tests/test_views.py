from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Review, Product


class ProductDetailReviewTest(TestCase):
    """Класс тестов представлений отзывов детальной страницы продукта"""

    fixtures = [
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
        "fixtures/16-reviews.json",
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="user", password="qwerty")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_view_context(self):
        """Тестирование передачи данных в контексте"""

        pk: int = 1
        reviews_context = Review.objects.filter(product__pk=pk)
        product_context = Product.objects.get(pk=pk)

        print(reviews_context, product_context)

        response = self.client.get(reverse("products:product", args=(pk,)))

        self.assertEqual(response.context["reviews"], reviews_context)
        self.assertEqual(response.context["product"], product_context)

    def test_view_post(self):
        """Тестирование отправки POST-запроса"""

        pk: int = 1
        form = {
            "text": "test review",
            "rating": 5,
        }

        response = self.client.post(reverse("products:product", args=(pk,)), data=form)
        self.assertEqual(response.context["success"], True)
