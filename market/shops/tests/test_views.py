from django.test import TestCase
from django.urls import reverse

from shops.models import Shop
from products.models import Banner


class ShopDetailViewTest(TestCase):
    """Класс тестов представлений деталей магазина"""

    fixtures = [
        "fixtures/04-shops.json",
        "fixtures/06-products.json",
        "fixtures/05-categories.json",
        "fixtures/08-offers.json",
    ]

    def test_shop_detail(self):
        pk = 35
        response = self.client.get(reverse("shops:shops_detail", args=[pk]))
        shop = Shop.objects.get(pk=pk)
        self.assertContains(response, shop.name)


class BannerInIndexPageViewTest(TestCase):
    """Класс тестов представления домашней страницы"""

    fixtures = [
        "fixtures/04-shops.json",
        "fixtures/05-categories.json",
        "fixtures/06-products.json",
        "fixtures/08-offers.json",
        "fixtures/11-product-images.json",
        "fixtures/15-banners.json",
        "fixtures/21-discount-products.json",
    ]

    @classmethod
    def setUpClass(cls):
        """Получение имен всех доступных url изображений баннеров"""

        super(BannerInIndexPageViewTest, cls).setUpClass()
        cls.images: list[str] = list(banner.image.url for banner in Banner.objects.all())

    def test_banners_in_page(self):
        """Проверка на наличие трех шаблонов в представлении, проверка статус-кода ответа"""

        response = self.client.get(reverse("shops:home"))
        self.assertEqual(response.status_code, 200)

        for image in self.images:
            if image in str(response.content):
                return True

        for _ in range(3):
            self.assertContains(response, "Slider-item")
