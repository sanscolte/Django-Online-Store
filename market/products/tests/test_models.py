from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.test import TestCase
from products.models import (
    Product,
    Detail,
    ProductDetail,
    Category,
    Banner,
    Review,
    ProductImage,
)


class ProductModelTest(TestCase):
    """Класс тестов модели Продукт"""

    @classmethod
    def setUpClass(cls):
        cls.detail = Detail.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.product.details.set([cls.detail])

    @classmethod
    def tearDownClass(cls):
        cls.detail.delete()
        cls.product.delete()

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

        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.banner = Banner.objects.create(product=cls.product, image="...static/img/content/home/slider.png")

    @classmethod
    def tearDownClass(cls):
        """Удаление сущности продукта и баннера"""

        cls.product.delete()
        cls.banner.delete()

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""

        banner = self.banner
        field_verboses = {
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

        cls.user = User.objects.create_user(email="user@email.ru", password="qwerty")
        cls.product = Product.objects.create(
            name="Тестовый продукт",
        )
        cls.review = Review.objects.create(
            product=cls.product,
            user=cls.user,
            text="Тестовый отзыв",
            rating=5,
        )

    @classmethod
    def tearDownClass(cls):
        """Удаление сущности пользователя, продукта и отзыва"""

        cls.user.delete()
        cls.product.delete()
        cls.review.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_verbose_name(self):
        """Тестирование валидности имени поля модели"""

        field_verboses = {
            "product": "Продукт",
            "user": "Пользователь",
            "text": "Отзыв",
            "rating": "Рейтинг",
        }

        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(self.review._meta.get_field(field).verbose_name, expected_value)

    def test_text_max_length(self):
        max_length = Review._meta.get_field("text").max_length
        self.assertEqual(max_length, 3000)

    def test_rating_max_length(self):
        validators = [validator for validator in self.review._meta.get_field("rating").validators]

        for validator in validators:
            if isinstance(validator, MinValueValidator):
                self.assertGreaterEqual(self.review.rating, validator.limit_value)
            elif isinstance(validator, MaxValueValidator):
                self.assertLessEqual(self.review.rating, validator.limit_value)


class ProductImageTest(TestCase):
    """
    Класс тестов модели Изображения продуктов
    """

    fixtures = ["05-categories.json", "06-products.json", "11-product-images.json"]

    def test_assert_expected_num_of_categories(self):
        self.assertEqual(ProductImage.objects.count(), 82)
