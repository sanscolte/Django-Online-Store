from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from products.models import Product, Category, HistoryProducts
from products.services.history_products_services import HistoryProductsService

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


class ProductDetailViewTest(TestCase):
    """Класс тестов представлений детальной страницы продукта"""

    fixtures = [
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
    ]

    def setUp(self):
        self.category = Category.objects.create(name="test category")
        self.product = Product.objects.create(name="test product", category=self.category)

    def test_product_detail_view_context(self):
        """Тестирование представления страницы с деталями продукта"""

        response = self.client.get(reverse("products:product-detail", args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product)


class HistoryProductsServiceTest(TestCase):
    """Класс тестов для сервиса истории просмотров продуктов"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)

    def test_add_product_to_history_if_not_exists(self):
        """Тест добавления продукта в историю просмотров если его там нет"""

        history_service = HistoryProductsService(self.product, self.user)
        history_service.add_product_history()
        self.assertEqual(HistoryProducts.objects.count(), 1)
        self.assertEqual(HistoryProducts.objects.first().product, self.product)

    def test_add_product_to_history_if_already_exists(self):
        """Тест добавления продукта в историю просмотров если он там уже есть"""

        history_service = HistoryProductsService(self.product, self.user)
        history_service.add_product_history()
        history_service.add_product_history()
        self.assertEqual(HistoryProducts.objects.count(), 1)
        self.assertEqual(HistoryProducts.objects.first().product, self.product)

    def test_check_product_in_history(self):
        """Тест добавления продукта в историю просмотров"""

        history_service = HistoryProductsService(self.product, self.user)
        history_service.add_product_history()
        self.assertTrue(history_service.check_product_in_history())


class HistoryProductsViewTest(TestCase):
    """Класс тестов для представления истории просмотров в профиле"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
    ]

    def setUp(self):
        """Добавление товара в историю просмотра"""

        self.history_product = HistoryProducts.objects.create(
            user=User.objects.get(pk=1),
            product=Product.objects.get(pk=1),
        )

    def test_history_products_view_context(self):
        """Тест контекста просмотренных товаров"""

        response = self.client.get(reverse("products:products-history"))
        history_products_list = response.context_data.get("history_products")
        history_product = history_products_list[0]

        self.assertEqual(response.status_code, 200)
        self.assertTrue("history_products" in response.context_data)
        self.assertEqual(len(history_products_list), 1)
        self.assertEqual(history_product.product.name, "iPhone")
