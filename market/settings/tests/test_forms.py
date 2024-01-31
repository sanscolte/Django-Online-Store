from django.test import TestCase
from settings.forms import SettingsForm, ClearCacheForm


class SettingsFormTests(TestCase):
    def test_settings_form_valid(self):
        data = {
            "min_order_price_for_free_shipping": 50.00,
            "standard_order_price": 10.00,
            "express_order_price": 20.00,
            "banners_count": 2,
            "days_offer": True,
            "top_items_count": 5,
            "limited_edition_count": 10,
            "product_cache_time": 3,
            "banner_cache_time": 3600,
            "product_list_cache_time": 1800,
        }

        form = SettingsForm(data=data)
        self.assertTrue(form.is_valid())

    def test_settings_form_invalid(self):
        data = {
            "min_order_price_for_free_shipping": "invalid_value",
            "standard_order_price": 10.00,
            "express_order_price": 20.00,
            "banners_count": 2,
            "days_offer": True,
            "top_items_count": 5,
            "limited_edition_count": 10,
            "product_cache_time": 3,
            "banner_cache_time": 3600,
            "product_list_cache_time": 1800,
        }

        form = SettingsForm(data=data)
        self.assertFalse(form.is_valid())


class ClearCacheFormTests(TestCase):
    def test_clear_cache_form_valid(self):
        data = {
            "clear_all_cache": True,
            "clear_product_detail_cache": True,
            "clear_product_list_cache": True,
        }

        form = ClearCacheForm(data=data)
        self.assertTrue(form.is_valid())
