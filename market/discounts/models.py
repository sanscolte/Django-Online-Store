from django.utils import timezone

from django.db import models

from products.models import Product, Category


class DiscountBase(models.Model):
    percentage = models.PositiveIntegerField(default=0, verbose_name="процент скидки")
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True

    def is_active(self):
        now = timezone.now().date()
        return self.start_date <= now <= self.end_date


class DiscountProduct(DiscountBase):
    products = models.ManyToManyField(Product, related_name="discount_products")


class DiscountSet(DiscountBase):
    categories = models.ManyToManyField(Category, related_name="discount_sets")
