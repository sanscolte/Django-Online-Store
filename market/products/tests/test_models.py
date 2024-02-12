from typing import Dict

from accounts.models import User
from django.test import TestCase
from products.models import (
    Product,
    Detail,
    ProductDetail,
    Category,
    Banner,
    Review,
    ProductImage,
    ProductsViews,
    ComparisonList,
)


class ProductModelTest(TestCase):
    """Класс тестов модели Продукт"""

    @classmethod
    def setUpTestData(cls):
        cls.detail = Detail.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.product.details.set([cls.detail])

    def test_verbose_name(self):
        product = ProductModelTest.product
        field_verboses = {
            "name": "наименование",
            "details": "характеристики",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(product._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        product = ProductModelTest.product
        max_length = product._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class DetailModelTest(TestCase):
    """Класс тестов модели Свойство продукта"""

    @classmethod
    def setUpClass(cls):
        cls.detail = Detail.objects.create(name="тестовая характеристика")

    @classmethod
    def tearDownClass(cls):
        cls.detail.delete()

    def test_verbose_name(self):
        detail = DetailModelTest.detail
        field_verboses = {
            "name": "наименование",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(detail._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        detail = DetailModelTest.detail
        max_length = detail._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class ProductDetailModelTest(TestCase):
    """Класс тестов модели Значение свойства продукта"""

    @classmethod
    def setUpClass(cls):
        cls.detail = Detail.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.product_detail = ProductDetail.objects.create(
            product=cls.product,
            detail=cls.detail,
            value="тестовое значение характеристики",
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.detail.delete()
        cls.product_detail.delete()

    def test_verbose_name(self):
        product_detail = ProductDetailModelTest.product_detail
        field_verboses = {
            "value": "значение",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(product_detail._meta.get_field(field).verbose_name, expected_value)

    def test_value_max_length(self):
        product_detail = ProductDetailModelTest.product_detail
        max_length = product_detail._meta.get_field("value").max_length
        self.assertEqual(max_length, 128)


class CategoryTest(TestCase):
    """
    Класс тестов модели Категория
    """

    fixtures = ["05-categories.json"]

    def test_assert_expected_num_of_categories(self):
        self.assertEqual(Category.objects.count(), 12)


class BannerModelTest(TestCase):
    """Класс тестов модели Banner"""

    @classmethod
    def setUpClass(cls):
        """Создание продукта и баннера с ним"""
        cls.product = Product.objects.create(name="Тестовый продукт")
        cls.banner = Banner.objects.create(product=cls.product, image="...static/img/content/home/slider.png")

    @classmethod
    def tearDownClass(cls):
        """Удаление сущности продукта и баннера"""
        cls.product.delete()
        cls.banner.delete()

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""
        banner = self.banner
        field_verboses: Dict[str, str] = {
            "image": "изображение",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(banner._meta.get_field(field).verbose_name, expected_value)


class ReviewModelTest(TestCase):
    """Класс тестов модели Review"""

    @classmethod
    def setUpClass(cls):
        """Создание пользователя, продукта и отзыва к нему"""
        cls.user: User = User.objects.create_user(email="user@email.ru", password="qwerty")
        cls.product: Product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.review: Review = Review.objects.create(
            product=cls.product,
            user=cls.user,
            text="Тестовый отзыв",
        )

    @classmethod
    def tearDownClass(cls):
        """Удаление сущности пользователя, продукта и отзыва"""
        cls.user.delete()
        cls.product.delete()
        cls.review.delete()

    def setUp(self):
        """Логин пользователя"""
        self.client.force_login(self.user)

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""
        field_verboses: Dict[str, str] = {
            "product": "Продукт",
            "user": "Пользователь",
            "text": "Отзыв",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(self.review._meta.get_field(field).verbose_name, expected_value)

    def test_text_max_length(self):
        """Тестирование максимально доступной длины поля text"""
        max_length: int = Review._meta.get_field("text").max_length
        self.assertEqual(max_length, 3000)


class ProductImageTest(TestCase):
    """
    Класс тестов модели Изображения продуктов
    """

    fixtures = ["05-categories.json", "06-products.json", "11-product-images.json"]

    def test_assert_expected_num_of_categories(self):
        self.assertEqual(ProductImage.objects.count(), 82)


class ProductsViewsTest(TestCase):
    """Класс тестов модели ProductsViews"""

    fixtures = [
        "01-users.json",
        "01-users-permissions.json",
        "01-groups.json",
        "05-categories.json",
        "06-products.json",
        "19-products-views.json",
    ]

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""
        views = ProductsViews.objects.first()

        field_verboses = {
            "product": "Продукт",
            "user": "Пользователь",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(views._meta.get_field(field).verbose_name, expected_value)

    def test_assert_expected_num_of_views(self):
        """Тестирование количества просмотров"""

        self.assertTrue(ProductsViews.objects.count() > 5)


class ComparisonListTest(TestCase):
    """Класс тестов для модели списка сравнения продуктов"""

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
        self.product1 = Product.objects.get(pk=1)
        self.product2 = Product.objects.get(pk=2)

    def test_comparison_list_creation(self):
        """Тестирование создания списка сравнения"""

        comparison_list = ComparisonList.objects.create(user=self.user)
        self.assertEqual(comparison_list.user, self.user)
        self.assertEqual(comparison_list.products.count(), 0)

    def test_add_product_to_comparison_list(self):
        """Тестирование добавления продуктов в список сравнения"""

        comparison_list = ComparisonList.objects.create(user=self.user)

        comparison_list.products.add(self.product1)
        comparison_list.products.add(self.product2)

        self.assertIn(self.product1, comparison_list.products.all())
        self.assertIn(self.product2, comparison_list.products.all())

    def test_remove_product_from_comparison_list(self):
        """Тестирование удаления продукта из списка сравнения"""

        comparison_list = ComparisonList.objects.create(user=self.user)
        comparison_list.products.add(self.product1)

        comparison_list.products.remove(self.product1)

        self.assertNotIn(self.product1, comparison_list.products.all())

    def test_clear_comparison_list(self):
        """Тестирование очистки списка сравнения"""

        comparison_list = ComparisonList.objects.create(user=self.user)
        comparison_list.products.add(self.product1, self.product2)

        comparison_list.products.clear()

        self.assertEqual(comparison_list.products.count(), 0)
