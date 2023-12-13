from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from products.models import Product, Category, ProductsViews
from products.services.products_views_services import ProductsViewsService

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


class ProductsViewsServiceTest(TestCase):
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

    def test_add_product_to_views_if_not_exists(self):
        """Тест добавления продукта в историю просмотров если его там нет"""

        views_service = ProductsViewsService(self.product, self.user)
        views_service.add_product_view()
        self.assertEqual(ProductsViews.objects.count(), 1)
        self.assertEqual(ProductsViews.objects.first().product, self.product)

    def test_add_product_to_views_if_already_exists(self):
        """Тест добавления продукта в историю просмотров если он там уже есть"""

        views_service = ProductsViewsService(self.product, self.user)
        views_service.add_product_view()
        views_service.add_product_view()
        self.assertEqual(ProductsViews.objects.count(), 1)
        self.assertEqual(ProductsViews.objects.first().product, self.product)

    def test_check_product_in_views(self):
        """Тест добавления продукта в историю просмотров"""

        views_service = ProductsViewsService(self.product, self.user)
        views_service.add_product_view()
        self.assertTrue(views_service.check_product_in_views())


class HistoryProductsViewTest(TestCase):
    """Класс тестов для представления истории просмотров в профиле"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
    ]

    def setUp(self):
        """Добавление товара в историю просмотра"""

        self.product_views = ProductsViews.objects.create(
            user=User.objects.get(pk=1),
            product=Product.objects.get(pk=1),
        )

    def test_products_view_context(self):
        """Тест контекста просмотренных товаров"""

        response = self.client.get(reverse("products:products-history"))
        products_views_list = response.context_data.get("products_views")
        history_product = products_views_list[0]

        self.assertEqual(response.status_code, 200)
        self.assertTrue("products_views" in response.context_data)
        self.assertEqual(len(products_views_list), 1)
        self.assertEqual(history_product.product.name, "iPhone")
