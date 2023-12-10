from unittest.mock import patch

from django.db.models import Avg
from django.db.models.functions import Round
from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from products.models import Product
from django.contrib.auth import get_user_model


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

    def test_view_with_reviews(self):
        """Тестирование контекста с отзывами"""

        pk: int = 1
        response = self.client.get(reverse("products:product-detail", args=[pk]))
        reviews = response.context_data.get("reviews")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("reviews" in response.context_data)
        self.assertEqual(reviews.number, 1)
        self.assertEqual(len(reviews), 3)

    def test_view_without_reviews(self):
        """Тестирование контекста без отзывов"""

        pk: int = 10
        response = self.client.get(reverse("products:product-detail", args=[pk]))
        reviews = response.context_data.get("reviews")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("reviews" in response.context_data)
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
