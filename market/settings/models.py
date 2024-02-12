from django.core.validators import MaxValueValidator
from django.db import models

from django.conf import settings
from settings.singleton_model import SingletonModel
from django.utils.translation import gettext_lazy as _


class SiteSetting(SingletonModel):
    """Модель настроек сайта"""

    name = models.CharField(default="Настройка сайта")
    min_order_price_for_free_shipping = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=settings.MIN_ORDER_PRICE_FOR_FREE_SHIPPING,
        verbose_name="minimum order price for free shipping, $",
    )
    standard_order_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=settings.STANDARD_ORDER_PRICE, verbose_name="standard order price, $"
    )
    express_order_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=settings.EXPRESS_ORDER_PRICE, verbose_name="express order price, $"
    )
    banners_count = models.PositiveIntegerField(
        validators=[MaxValueValidator(3)], default=settings.BANNERS_COUNT, verbose_name="banners count"
    )
    days_offer = models.BooleanField(verbose_name="show days offer", default=True)
    top_items_count = models.PositiveIntegerField(
        validators=[MaxValueValidator(8)], default=settings.TOP_ITEMS_COUNT, verbose_name="top items count"
    )
    limited_edition_count = models.PositiveIntegerField(
        validators=[MaxValueValidator(16)],
        default=settings.LIMITED_EDITION_COUNT,
        verbose_name="limited edition count",
    )
    product_cache_time = models.PositiveIntegerField(
        default=settings.CACHE_TIME_DETAIL_PRODUCT_PAGE / 86400, verbose_name="product cache time, days"
    )
    banner_cache_time = models.PositiveIntegerField(
        default=settings.BANNER_CACHE_TIME, verbose_name="banner cache time"
    )
    product_list_cache_time = models.PositiveIntegerField(
        default=settings.PRODUCT_LIST_CACHE_TIME, verbose_name="product list cache time"
    )

    def __str__(self) -> str:
        return "Настройки сайта"

    class Meta:
        verbose_name_plural = _("Настройки")
        verbose_name = _("Настройка")
