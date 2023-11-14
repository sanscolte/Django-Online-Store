from django.db import models
from django.utils.translation import gettext_lazy as _


def banner_preview_directory_path(instance: "Banner", filename: str) -> str:
    return "banners/{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))


class Detail(models.Model):
    """Свойство продукта"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))


class ProductDetail(models.Model):
    """Значение свойства продукта"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    value = models.CharField(max_length=128, verbose_name=_("значение"))

    class Meta:
        constraints = [models.UniqueConstraint("product", "detail", name="unique_detail_for_product")]


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="banners")
    image = models.ImageField(upload_to=banner_preview_directory_path)
    is_active = models.BooleanField(default=True)
