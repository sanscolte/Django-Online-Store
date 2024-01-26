from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from settings.models import SiteSetting


class SettingsViewTests(TestCase):
    def setUp(self):
        self.site_setting = SiteSetting.objects.create(name="Test Setting")

    def test_settings_view_get(self):
        response = self.client.get(reverse("settings:site-settings"))
        self.assertEqual(response.status_code, 200)

    def test_settings_view_post(self):
        data = {
            "min_order_price_for_free_shipping": 60.00,
            "standard_order_price": 15.00,
            "express_order_price": 25.00,
            "banners_count": 3,
            "days_offer": False,
            "top_items_count": 8,
            "limited_edition_count": 15,
            "product_cache_time": 5,
            "banner_cache_time": 7200,
            "product_list_cache_time": 2700,
        }
        response = self.client.post(reverse("settings:site-settings"), data)
        self.assertEqual(response.status_code, 200)

        updated_site_setting = SiteSetting.objects.first()
        self.assertEqual(updated_site_setting.min_order_price_for_free_shipping, 60.00)
        self.assertEqual(updated_site_setting.standard_order_price, 15.00)
        self.assertEqual(updated_site_setting.express_order_price, 25.00)

    def test_clear_all_cache(self):
        cache.set("test_key", "test_value")
        self.assertEqual(cache.get("test_key"), "test_value")
        self.client.post(reverse("settings:site-settings"), {"clear_all_cache": "on"})
        self.assertIsNone(cache.get("test_key"))

    def test_clear_cache_for_some_pages(self):
        cache.set("product_detail_key", "product_detail_value")
        self.assertEqual(cache.get("product_detail_key"), "product_detail_value")
        self.client.post(reverse("settings:site-settings"), {"clear_product_detail_cache": "on"})
        self.assertIsNone(cache.get("product_detail_key"))

    def test_get_settings_dict(self):
        response = self.client.get(reverse("settings:site-settings"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("settings_dict", response.context_data)
        settings = response.context_data["settings_dict"]
        self.assertIsInstance(settings, dict)
