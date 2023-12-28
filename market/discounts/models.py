from django.utils import timezone

from django.db import models

from products.models import Product, Category

from django.core.validators import MinValueValidator, MaxValueValidator


class DiscountBase(models.Model):
    name = models.CharField(max_length=100, verbose_name="наименование события")
    percentage = models.PositiveIntegerField(default=0, verbose_name="процент скидки")
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True

    def is_active(self):
        now = timezone.now().date()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"percentage={self.percentage}, event={self.name}"


class DiscountProduct(DiscountBase):
    products = models.ManyToManyField(Product, related_name="discount_products")

    class Meta:
        verbose_name = "Скидка для продукта"
        verbose_name_plural = "Скидки для продуктов"


class DiscountSet(DiscountBase):
    categories = models.ManyToManyField(Category, related_name="discount_sets")
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="вес скидки",
        validators=[MinValueValidator(0.01), MaxValueValidator(1.00)],
    )

    class Meta:
        verbose_name = "Скидка для набора"
        verbose_name_plural = "Скидки на наборов"


class DiscountCart(DiscountBase):
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="вес скидки",
        validators=[MinValueValidator(0.01), MaxValueValidator(1.00)],
    )

    class Meta:
        verbose_name = "Скидка для корзины"
        verbose_name_plural = "Скидки для корзины"
