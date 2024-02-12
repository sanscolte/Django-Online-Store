from django.core.exceptions import ValidationError
from django.test import TestCase
from settings.models import SiteSetting


class SiteSettingModelTests(TestCase):
    def setUp(self):
        self.site_setting = SiteSetting.objects.create(
            name="Test Setting",
            min_order_price_for_free_shipping=50.00,
            standard_order_price=10.00,
            express_order_price=20.00,
            banners_count=2,
            days_offer=True,
            top_items_count=5,
            limited_edition_count=10,
            product_cache_time=3,
            banner_cache_time=3600,
            product_list_cache_time=1800,
        )

    def test_str_method(self):
        self.assertEqual(str(self.site_setting), "site settings")

    def test_verbose_name_plural(self):
        self.assertEqual(str(SiteSetting._meta.verbose_name_plural), "settings")

    def test_verbose_name(self):
        self.assertEqual(str(SiteSetting._meta.verbose_name), "setting")

    def test_values(self):
        self.assertEqual(self.site_setting.name, "Test Setting")
        self.assertEqual(self.site_setting.min_order_price_for_free_shipping, 50.00)
        self.assertEqual(self.site_setting.standard_order_price, 10.00)
        self.assertEqual(self.site_setting.express_order_price, 20.00)
        self.assertEqual(self.site_setting.banners_count, 2)
        self.assertEqual(self.site_setting.days_offer, True)
        self.assertEqual(self.site_setting.top_items_count, 5)
        self.assertEqual(self.site_setting.limited_edition_count, 10)
        self.assertEqual(self.site_setting.product_cache_time, 3)
        self.assertEqual(self.site_setting.banner_cache_time, 3600)
        self.assertEqual(self.site_setting.product_list_cache_time, 1800)

    def test_max_value_validator(self):
        with self.assertRaises(ValidationError):
            self.site_setting.banners_count = 4
            self.site_setting.full_clean()
            self.site_setting.save()
