from unittest.mock import patch

from django.db.models import Avg
from django.db.models.functions import Round
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import Client

from products.models import Product, ProductsViews, ComparisonList, ProductImport
from products.services.products_views_services import ProductsViewsService
from products.tasks import import_products

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
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
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
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
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
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
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
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
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
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
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
        self.client = Client()
        self.client.force_login(self.user)
        self.product_1 = Product.objects.create(name="Test Product 1")
        self.product_2 = Product.objects.create(name="Test Product 2")
        self.product_3 = Product.objects.create(name="Test Product 3")
        self.product_4 = Product.objects.create(name="Test Product 4")
        self.comparison_list, _ = ComparisonList.objects.get_or_create(user=self.user)
        session = self.client.session
        session["comparison_list_id"] = self.comparison_list.id
        session.save()

    def test_get_comparison_list_creates_comparison_list(self):
        """Тестирование создания списка сравнения для пользователя"""

        self.client.force_login(self.user)
        response = self.client.get(reverse("products:comparison-list"))
        self.assertEqual(response.status_code, 200)

        comparison_list_id = self.client.session.get("comparison_list_id")
        self.assertIsNotNone(comparison_list_id)

        comparison_list = ComparisonList.objects.get(id=comparison_list_id, user=self.user)
        self.assertIsNotNone(comparison_list)


class ComparisonListViewTest(TestCase):
    """Класс тестов для представления списка сравнения продуктов"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
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
    """Класс тестов для представления добавления продуктов в список сравнения"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.product = Product.objects.create(name="Test Product")
        self.comparison_list, _ = ComparisonList.objects.get_or_create(user=self.user)
        session = self.client.session
        session["comparison_list_id"] = self.comparison_list.id
        session.save()

    def test_add_to_comparison_list(self):
        data = {
            "product_id": self.product.pk,
            "action": "add_to_comparison",
        }

        response = self.client.post(reverse_lazy("products:add-to-list", kwargs={"pk": self.product.pk}), data)
        self.assertTrue(self.comparison_list.products.filter(pk=self.product.pk).exists())
        self.assertEqual(response.status_code, 302)


class RemoveFromComparisonListViewTest(TestCase):
    """Класс тестов для представления удаления продуктов из списка сравнения"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.product = Product.objects.create(name="Test Product")
        self.client = Client()
        self.client.force_login(self.user)
        self.comparison_list, _ = ComparisonList.objects.get_or_create(user=self.user)
        session = self.client.session
        session["comparison_list_id"] = self.comparison_list.id
        session.save()

    def test_remove_from_comparison_list(self):
        self.comparison_list.products.add(self.product)

        data = {
            "action": "remove_from_comparison",
            "product_id": self.product.pk,
        }

        response = self.client.post(reverse("products:remove-from-list", kwargs={"pk": self.product.pk}), data)
        self.assertFalse(self.comparison_list.products.filter(pk=self.product.pk).exists())
        self.assertEqual(response.status_code, 302)


def get_admin_change_view_url(obj: Product) -> str:
    return reverse("admin:{}_{}_change".format(obj._meta.app_label, type(obj).__name__.lower()), args=(obj.pk,))


class ImportProductsViewTest(TestCase):
    """Класс тестов для представления импорта продуктов"""

    @patch("products.admin.import_products.delay", import_products)
    def test_valid_file_import(self):
        """Тест загрузки валидного файла"""
        filename: str = "test_valid_file.json"
        file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)

        with open(file_path, "rb") as file:
            uploaded_file = SimpleUploadedFile(filename, file.read())

        url: str = "/ru/admin/products/product/import-products/"
        data = {
            "json_files": uploaded_file,
        }
        response = self.client.post(url, data)
        saved_filename = ProductImport.objects.latest("pk").file.name[7:]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 5)
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/success/{saved_filename}")))
        self.assertEqual(response.context["status"], "Выполнен")

        # удаляем созданную копию загруженного файла
        os.remove(os.path.join(settings.MEDIA_ROOT, f"import/success/{saved_filename}"))

    @patch("products.admin.import_products.delay", import_products)
    def test_invalid_file_import(self):
        """Тест загрузки невалидного файла"""
        filename: str = "test_invalid_file.json"
        file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)

        with open(file_path, "rb") as file:
            uploaded_file = SimpleUploadedFile(filename, file.read())

        url: str = "/ru/admin/products/product/import-products/"
        data = {
            "json_files": uploaded_file,
        }
        response = self.client.post(url, data)
        saved_filename = ProductImport.objects.latest("pk").file.name[7:]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 0)
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/fail/{saved_filename}")))
        self.assertEqual(response.context["status"], "Завершён с ошибкой")

        # удаляем созданную копию загруженного файла
        os.remove(os.path.join(settings.MEDIA_ROOT, f"import/fail/{saved_filename}"))

    @patch("products.admin.import_products.delay", import_products)
    def test_multiple_file_import(self):
        """Тест загрузки нескольких файлов разом"""
        filenames: list[str] = ["test_valid_file.json", "test_invalid_file.json"]
        files: list = []

        for filename in filenames:
            file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)
            with open(file_path, "rb") as file:
                uploaded_file = SimpleUploadedFile(filename, file.read())
                files.append(uploaded_file)

        url: str = "/ru/admin/products/product/import-products/"
        data = {
            "json_files": files,
        }
        response = self.client.post(url, data, follow=True)

        latest_products = ProductImport.objects.all().order_by("-pk")[:2]
        valid_filename = latest_products[1].file.name[7:]
        invalid_filename = latest_products[0].file.name[7:]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 5)
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/success/{valid_filename}")))
        self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/fail/{invalid_filename}")))
        self.assertEqual(response.context["status"], "Завершён с ошибкой")

        # удаляем созданную копию загруженного файла
        os.remove(os.path.join(settings.MEDIA_ROOT, f"import/success/{valid_filename}"))
        os.remove(os.path.join(settings.MEDIA_ROOT, f"import/fail/{invalid_filename}"))

    @patch("products.admin.import_products.delay", import_products)
    def test_empty_file_import(self):
        """Тест загрузки пустого файла"""
        filename: str = "test_empty_file.json"
        file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)

        with open(file_path, "rb") as file:
            uploaded_file = SimpleUploadedFile(filename, file.read())

        url: str = "/en/admin/products/product/import-products/"
        data = {
            "json_files": uploaded_file,
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("The submitted file is empty" in str(response.context))
