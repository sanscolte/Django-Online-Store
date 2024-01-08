from datetime import timedelta
from django.utils import timezone
from django.test import TestCase

from discounts.models import DiscountSet, DiscountProduct
from products.models import Category, Product


class DiscountSetTest(TestCase):
    """Класс тестов модели DiscountSet"""

    def setUp(self):
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")

        self.discount_set = DiscountSet.objects.create(
            percentage=10,
            weight=0.02,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=7),
        )

        self.discount_set.categories.add(self.category1, self.category2)

    def tearDown(self):
        self.category1.delete()
        self.category2.delete()
        self.discount_set.delete()

    def test_discount_set_categories(self):
        self.assertEqual(self.discount_set.categories.count(), 2)
        self.assertIn(self.category1, self.discount_set.categories.all())
        self.assertIn(self.category2, self.discount_set.categories.all())

    def test_discount_set_creation(self):
        self.assertIsInstance(self.discount_set, DiscountSet)
        self.assertEqual(self.discount_set.percentage, 10)

    def test_discount_set_active(self):
        self.assertTrue(self.discount_set.is_active())

    def test_discount_set_inactive(self):
        self.discount_set.end_date = self.discount_set.start_date - timedelta(days=1)
        self.discount_set.save()
        self.assertFalse(self.discount_set.is_active())


class DiscountProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product")
        self.discount_product = DiscountProduct.objects.create(
            percentage=20, start_date=timezone.now().date(), end_date=timezone.now().date() + timedelta(days=7)
        )
        self.discount_product.products.add(self.product)

    def tearDown(self):
        self.product.delete()
        self.discount_product.delete()

    def test_is_active(self):
        """Проверяем, что активная скидка возвращает True"""
        today = timezone.now().date()
        self.discount_product.start_date = today - timedelta(days=1)
        self.discount_product.end_date = today + timedelta(days=1)
        self.discount_product.save()
        self.assertTrue(self.discount_product.is_active())

    def test_products(self):
        """Проверяем, что продукты добавлены к скидке"""
        self.assertEqual(self.discount_product.products.count(), 1)
        self.assertEqual(self.discount_product.products.first(), self.product)
