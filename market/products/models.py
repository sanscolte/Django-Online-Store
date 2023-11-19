from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import datetime


class Category(models.Model):
    """Категория"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"), unique=True)
    description = models.TextField(verbose_name=_("описание"), blank=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_index = models.CharField(verbose_name=_("индекс сортировки"), blank=True)

    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        return self.description[:50] + "..."

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    description = models.TextField(verbose_name=_("описание"), blank=True)
    date_of_publication = models.DateTimeField(default=datetime.now())
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))

    @property
    def num_of_purchases(self):
        return 0

    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        return self.description[:50] + "..."

    @property
    def min_price(self) -> Decimal:
        """Вычисляет минимальную цену на товар среди магазинов, в которых он продается."""

        prices = self.offers.values_list("price")
        assert len(prices) > 0, "Товар не продается ни в одном из магазинов. Невозможно вычислить минимальную цену."

        return min(prices)

    def __str__(self) -> str:
        return f"{self.name}"


class Detail(models.Model):
    """Свойство продукта"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))


class ProductDetail(models.Model):
    """Значение свойства продукта"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name=_("характеристика"), default=0)
    value = models.CharField(max_length=128, verbose_name=_("значение"))

    class Meta:
        constraints = [models.UniqueConstraint("product", "detail", name="unique_detail_for_product")]


class ProductImage(models.Model):
    """Фотографии продукта"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_("изображение"), default=1)
    sort_image = models.IntegerField()


def banner_preview_directory_path(instance: "Banner", filename: str) -> str:
    return "banners/{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="banners")
    image = models.ImageField(upload_to=banner_preview_directory_path)
    is_active = models.BooleanField(default=True)
