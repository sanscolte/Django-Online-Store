import glob
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.test import Client

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


def get_admin_change_view_url(obj: Product) -> str:
    return reverse("admin:{}_{}_change".format(obj._meta.app_label, type(obj).__name__.lower()), args=(obj.pk,))


class ImportProductsViewTest(TestCase):
    """Класс тестов для представления импорта продуктов"""

    def setUp(self):
        client = Client()
        client.login(username="demon_at@mail.ru", password="61903991shalaikodima")

    def test_valid_file_import(self):
        filename = "test_valid_file.json"
        file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)

        with open(file_path, "rb") as file:
            uploaded_file = SimpleUploadedFile(filename, file.read())

        url = "/admin/products/product/import-products/"
        data = {
            "json_files": uploaded_file,
            "email": "test@example.com",
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Exception):
            self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/success/{filename}")))
            self.assertEqual(response.context["email"], "test@example.com")
            self.assertEqual(response.context["status"], "Выполнен")
            self.assertRedirects(response, url, status_code=302)

        # удаляем созданную копию загруженного файла
        files_to_delete = glob.glob(os.path.join(settings.MEDIA_ROOT, "test_valid_file*.json"))
        for file_to_delete in files_to_delete:
            os.remove(file_to_delete)

    def test_invalid_file_import(self):
        filename = "test_invalid_file.json"
        file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)

        with open(file_path, "rb") as file:
            uploaded_file = SimpleUploadedFile(filename, file.read())

        url = "/admin/products/product/import-products/"
        data = {
            "json_files": uploaded_file,
            "email": "test@example.com",
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Exception):
            self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/fail/{filename}")))
            self.assertEqual(response.context["email"], "test@example.com")
            self.assertEqual(response.context["status"], "Завершён с ошибкой")
            self.assertRedirects(response, url, status_code=302)

        # удаляем созданную копию загруженного файла
        files_to_delete = glob.glob(os.path.join(settings.MEDIA_ROOT, "test_invalid_file*.json"))
        for file_to_delete in files_to_delete:
            os.remove(file_to_delete)

    def test_multiple_file_import(self):
        filenames = ["test_valid_file.json", "test_invalid_file.json"]
        files = []

        for filename in filenames:
            file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)
            with open(file_path, "rb") as file:
                uploaded_file = SimpleUploadedFile(filename, file.read())
                files.append(uploaded_file)

        url = "/admin/products/product/import-products/"
        data = {
            "json_files": files,
            "email": "test@example.com",
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Exception):
            new_valid_files = glob.glob(os.path.join(settings.MEDIA_ROOT, "import/success/test_valid_file_*.json"))
            new_invalid_files = glob.glob(os.path.join(settings.MEDIA_ROOT, "import/fail/test_invalid_file_*.json"))
            new_files = new_valid_files + new_invalid_files
            for new_file in new_files:
                self.assertTrue(os.path.exists(new_file))
            self.assertEqual(response.context["email"], "test@example.com")
            self.assertEqual(response.context["status"], "Завершён с ошибкой")
            self.assertRedirects(response, url, status_code=302)

        # удаляем созданную копию загруженного файла
        valid_files_to_delete = glob.glob(os.path.join(settings.MEDIA_ROOT, "test_valid_file*.json"))
        invalid_files_to_delete = glob.glob(os.path.join(settings.MEDIA_ROOT, "test_invalid_file*.json"))
        files_to_delete = valid_files_to_delete + invalid_files_to_delete
        for file_to_delete in files_to_delete:
            os.remove(file_to_delete)

    def test_concurrent_import(self):
        filename = "test_valid_file.json"
        file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)

        with open(file_path, "rb") as file:
            uploaded_file = SimpleUploadedFile(filename, file.read())

        url = "/admin/products/product/import-products/"
        data = {
            "json_files": uploaded_file,
            "email": "test@example.com",
        }
        fst_response = self.client.post(url, data, follow=True)
        snd_response = self.client.post(url, data, follow=True)

        self.assertEqual(fst_response.status_code, 200)

        with self.assertRaises(Exception):
            self.assertEqual(snd_response.status_code, 400)
            self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/success/{filename}")))
            self.assertEqual(fst_response.context["email"], "test@example.com")
            self.assertEqual(fst_response.context["status"], "Выполнен")
            self.assertEqual(snd_response.context["status"], "В процессе выполнения")
            self.assertRedirects(fst_response, url, status_code=302)

        # удаляем созданную копию загруженного файла
        files_to_delete = glob.glob(os.path.join(settings.MEDIA_ROOT, "test_valid_file*.json"))
        for file_to_delete in files_to_delete:
            os.remove(file_to_delete)

    def test_empty_file_import(self):
        filename = "test_empty_file.json"
        file_path = os.path.join(os.path.dirname(__file__), "test_files", filename)

        with open(file_path, "rb") as file:
            uploaded_file = SimpleUploadedFile(filename, file.read())

        url = "/admin/products/product/import-products/"
        data = {
            "json_files": uploaded_file,
            "email": "test@example.com",
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        with self.assertRaises(Exception):
            with self.assertRaises(ValidationError):
                pass
            self.assertTrue(os.path.exists(os.path.join(settings.MEDIA_ROOT, f"import/fail/{filename}")))
            self.assertEqual(response.context["email"], "test@example.com")
            self.assertEqual(response.context["status"], "Завершён с ошибкой")
            self.assertRedirects(response, url, status_code=302)

        # удаляем созданную копию загруженного файла
        files_to_delete = glob.glob(os.path.join(settings.MEDIA_ROOT, "test_empty_file*.json"))
        for file_to_delete in files_to_delete:
            os.remove(file_to_delete)
