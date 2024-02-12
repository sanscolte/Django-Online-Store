from django.test import TestCase

from products.forms import ReviewForm, ProductDetailForm
from products.models import Review, Product, Detail


class ReviewFormTest(TestCase):
    """Класс тестов для формы Review"""

    def test_valid_form(self):
        """Тестирование валидной формы"""
        data: dict[str, int] = {"text": "test review", "rating": 5}
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_text_form(self):
        """Тестирование формы с текстом превышающем валидное значение"""

        max_length: int = int(Review._meta.get_field("text").max_length) + 1
        text: str = "_" * max_length
        data: dict[str, int] = {"text": text, "rating": 5}
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())


class ProductDetailFormTest(TestCase):
    """Класс тестов для формы ProductDetail"""

    def test_valid_product_details_form(self):
        product = Product.objects.create(name="test product")
        detail = Detail.objects.create(name="test detail")
        data = {"product": product.pk, "detail": detail.pk, "value": "test value"}
        form = ProductDetailForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_product_details_form(self):
        data = {"product": "", "detail": "", "value": ""}
        form = ProductDetailForm(data=data)
        self.assertFalse(form.is_valid())
