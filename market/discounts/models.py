from django.utils import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product, Category

from django.core.validators import MinValueValidator, MaxValueValidator


class DiscountBase(models.Model):
    """Базовая модель скидок"""

    name = models.CharField(max_length=100, verbose_name=_("наименование события"))
    percentage = models.PositiveIntegerField(default=0, verbose_name=_("процент скидки"))
    start_date = models.DateField(verbose_name=_("начало действия"))
    end_date = models.DateField(verbose_name=_("окончание действия"))

    class Meta:
        abstract = True

    def is_active(self):
        now = timezone.now().date()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"percentage={self.percentage}, event={self.name}"


class DiscountProduct(DiscountBase):
    """Скидка на продукт"""

    products = models.ManyToManyField(Product, related_name="discount_products")

    class Meta:
        verbose_name = _("Скидка для продукта")
        verbose_name_plural = _("Скидки для продуктов")


class DiscountSet(DiscountBase):
    """Скидка на набор"""

    categories = models.ManyToManyField(Category, related_name="discount_sets")
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name=_("вес скидки"),
        validators=[MinValueValidator(0.01), MaxValueValidator(1.00)],
    )

    class Meta:
        verbose_name = _("Скидка для набора")
        verbose_name_plural = _("Скидки на наборов")


class DiscountCart(DiscountBase):
    """Скидка на корзину"""

    weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name=_("вес скидки"),
        validators=[MinValueValidator(0.01), MaxValueValidator(1.00)],
    )
    price_from = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("диапазон цены от"))
    price_to = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("диапазон цены до"))

    class Meta:
        verbose_name = _("Скидка для корзины")
        verbose_name_plural = _("Скидки для корзины")
