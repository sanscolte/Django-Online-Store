from unittest.mock import patch

from django.db.models import Avg
from django.db.models.functions import Round
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from products.models import Product, ProductsViews, ComparisonList
from products.services.products_views_services import ProductsViewsService
from products.views import BaseComparisonView

User = get_user_model()


class TestProductListView(TestCase):
    """Класс тестов представлений продуктов"""

    fixtures = [
        "04-shops.json",
        "05-categories.json",
        "06-products.json",
        "08-offers.json",
        "11-product-images.json",
    ]

    def setUp(self) -> None:
        cache.clear()

    def test_filter_name_iexact(self):
        """Проверка фильтра по наименованию продукта"""

        url = reverse("products:product-list") + "?name__iexact=smeg"
        response = self.client.get(url)
        product_count = Product.objects.filter(name="Smeg").count()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smeg")
        self.assertEqual(product_count, 1)

    @patch("products.views.ProductListView.paginate_by", None)
    def test_filter_avg_price_in_range(self):
        """Проверка фильтра по диапазону цен. Пагинация отключена в декораторе."""

        min_price = 1_000
        max_price = 10_000

        url = reverse("products:product-list") + f"?avg_price__gte={min_price}&avg_price__lte={max_price}"
        response = self.client.get(url)
        product_count = (
            Product.objects.annotate(avg_price=Round(Avg("offers__price"), 2))
            .filter(avg_price__gte=min_price, avg_price__lte=max_price)
            .count()
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["object_list"]), product_count)

    def test_avg_price_asc_ordering(self):
        """Проверка сортировки по средней цене по возрастанию."""

        url = reverse("products:product-list") + "?o=avg_price"
        response = self.client.get(url)
        products = response.context_data["object_list"]

        for idx in range(1, len(products)):
            self.assertTrue(products[idx].avg_price >= products[idx - 1].avg_price)

    def test_avg_price_desc_ordering(self):
        """Проверка сортировки по средней цене по убыванию."""

        url = reverse("products:product-list") + "?o=-avg_price"
        response = self.client.get(url)
        products = response.context_data["object_list"]

        for idx in range(1, len(products)):
            self.assertTrue(products[idx].avg_price <= products[idx - 1].avg_price)

    def test_reviews_count_desc_ordering(self):
        """Проверка сортировки по количеству отзывов по убыванию."""

        url = reverse("products:product-list") + "?o=-reviews_count"
        response = self.client.get(url)
        products = response.context_data["object_list"]

        for idx in range(1, len(products)):
            self.assertTrue(products[idx].reviews_count <= products[idx - 1].reviews_count)

    def test_reviews_count_asc_ordering(self):
        """Проверка сортировки по количеству отзывов по возрастанию."""

        url = reverse("products:product-list") + "?o=reviews_count"
        response = self.client.get(url)
        products = response.context_data["object_list"]

        for idx in range(1, len(products)):
            self.assertTrue(products[idx].reviews_count >= products[idx - 1].reviews_count)

    def test_date_of_publication_ordering(self):
        """Проверка сортировки по дате публикации"""

        url = reverse("products:product-list") + "?o=publication"
        response = self.client.get(url)
        products = response.context_data["object_list"]

        for idx in range(1, len(products)):
            self.assertTrue(products[idx].date_of_publication >= products[idx - 1].date_of_publication)

    def test_product_image_url(self):
        """Проверка формирования preview продукта"""

        url = reverse("products:product-list") + "?name__iexact=smeg"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object_list"][0].image, "/uploads/products/Smeg/smeg1.jpg")


class ProductDetailReviewTest(TestCase):
    """Класс тестов представлений отзывов детальной страницы продукта"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
        "fixtures/16-reviews.json",
        "fixtures/17-details.json",
        "fixtures/18-product-details.json",
        "fixtures/19-products-views.json",
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
        review_form: dict[str, int | str] = {"text": "test review", "rating": 5, "action": "add_review"}

        response = self.client.post(
            reverse("products:product-detail", args=(pk,)),
            data=review_form,
        )
        self.assertIsNotNone(response)

        self.assertRedirects(response, reverse("products:product-detail", args=(pk,)))


class ProductDetailViewTest(TestCase):
    """Класс тестов представлений детальной страницы продукта"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)

    def test_product_detail_view_context(self):
        """Тестирование представления страницы с деталями продукта"""

        self.client.force_login(self.user)

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


class BaseComparisonViewTest(TestCase):
    """Класс тестов для базового представления списка сравнения продуктов"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
        "fixtures/08-offers.json",
        "fixtures/17-details.json",
        "fixtures/18-product-details.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.product = Product.objects.get(pk=1)

    def test_get_comparison_list_creates_comparison_list(self):
        """Тестирование создания списка сравнения для пользователя"""

        self.client.force_login(self.user)
        response = self.client.get(reverse("products:comparison-list"))
        self.assertEqual(response.status_code, 200)

        comparison_list_id = self.client.session.get("comparison_list_id")
        self.assertIsNotNone(comparison_list_id)

        comparison_list = ComparisonList.objects.get(id=comparison_list_id, user=self.user)
        self.assertIsNotNone(comparison_list)

    def test_get_comparison_count_returns_correct_count(self):
        """Тестирование правильного подсчёта продуктов, находящихся в списке сравнения"""

        self.client.force_login(self.user)
        response = self.client.get(reverse("products:comparison-list"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("products_in_comparison", response.context_data)
        self.assertEqual(len(response.context_data["products_in_comparison"]), 0)

        comparison_list_id = self.client.session.get("comparison_list_id")
        comparison_list = ComparisonList.objects.get(id=comparison_list_id, user=self.user)
        comparison_list.products.add(self.product)

        response = self.client.get(reverse("products:comparison-list"))

        self.assertIn("products_in_comparison", response.context_data)
        self.assertEqual(len(response.context_data["products_in_comparison"]), 1)


class ComparisonListViewTest(TestCase):
    """Класс тестов для представления списка сравнения продуктов"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
        "fixtures/08-offers.json",
        "fixtures/17-details.json",
        "fixtures/18-product-details.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.comparison_list = ComparisonList.objects.create(user=self.user)

    def test_get_context_data(self):
        """Тестирование получения контекстной информации"""

        self.client.force_login(self.user)
        response = self.client.get(reverse("products:comparison-list"))
        self.assertEqual(response.status_code, 200)

        context = response.context_data
        self.assertIn("products_in_comparison", context)
        self.assertIn("product_details_in_comparison", context)


class AddToComparisonListViewTest(TestCase):
    fixtures = [
        "fixtures/01-users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.product_1 = Product.objects.create(name="Test Product 1")
        self.product_2 = Product.objects.create(name="Test Product 2")
        self.product_3 = Product.objects.create(name="Test Product 3")
        self.product_4 = Product.objects.create(name="Test Product 4")
        self.comparison_list_id = self.client.session.get("comparison_list_id")
        self.comparison_list, created = ComparisonList.objects.get_or_create(
            id=self.comparison_list_id, user=self.user
        )
        self.comparison_count = BaseComparisonView.get_comparison_count(self.client.request.user, self.client.request)

    def test_add_to_comparison_list(self):
        data = {
            "product_id": self.product_1.pk,
            "action": "add_to_comparison",
        }
        response = self.client.post(reverse_lazy("products:add-to-list", kwargs={"pk": self.product_1.pk}), data)
        self.assertTrue(self.comparison_list.products.filter(pk=self.product_1.pk).exists())
        self.assertEqual(response.status_code, 302)

    def test_max_products_to_comparison_list(self):
        self.assertFalse(self.comparison_count)
        self.comparison_list.products.add(self.product_1)
        self.assertIn(self.product_1, self.comparison_list.products.all())
        self.assertTrue(self.comparison_count)
        self.comparison_list.products.add(self.product_2)
        self.assertIn(self.product_2, self.comparison_list.products.all())
        self.comparison_list.products.add(self.product_3)
        self.assertTrue(self.comparison_count)
        self.assertIn(self.product_3, self.comparison_list.products.all())
        self.comparison_list.products.add(self.product_4)
        self.assertFalse(self.comparison_count)
        self.assertNotIn(self.product_4, self.comparison_list.products.all())


class RemoveFromComparisonListViewTest(TestCase):
    fixtures = [
        "fixtures/01-users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.product = Product.objects.create(name="Test Product")
        self.client = Client()
        self.client.force_login(self.user)
        self.comparison_list_id = self.client.session.get("comparison_list_id")
        self.comparison_list, created = ComparisonList.objects.get_or_create(
            id=self.comparison_list_id, user=self.user
        )

    def test_remove_from_comparison_list(self):
        self.client.force_login(self.user)
        self.comparison_list.products.add(self.product)

        response_get = self.client.get(reverse("products:remove-from-list", kwargs={"pk": self.product.pk}))
        self.assertEqual(response_get.status_code, 200)

        self.assertTrue(self.user.is_authenticated)

        data = {
            "csrfmiddlewaretoken": self.client.cookies["csrftoken"].value,
            "action": "remove_from_comparison",
            "product_id": self.product.pk,
        }

        response = self.client.post(reverse("products:remove-from-list", kwargs={"pk": self.product.pk}), data)
        self.assertFalse(self.comparison_list.products.filter(pk=self.product.pk).exists())
        self.assertEqual(response.status_code, 302)
