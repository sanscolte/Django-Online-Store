from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import shop_preivew_directory_path


class Shop(models.Model):
    """Магазин"""

    name = models.CharField(max_length=512, verbose_name=_("название"))
    products = models.ManyToManyField(
        "products.Product",
        through="Offer",
        related_name="shops",
        verbose_name=_("товары в магазине"),
    )
    description = models.CharField(max_length=1000, verbose_name="описание")
    image = models.ImageField(
        upload_to=shop_preivew_directory_path, blank=True, null=True, verbose_name="изображение товара"
    )
    phone = models.CharField(max_length=128, verbose_name=_("телефон"))
    address = models.CharField(max_length=512, verbose_name=_("адрес"))
    email = models.EmailField(verbose_name=_("email"))


class Offer(models.Model):
    """Предложение магазина"""

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))

    class Meta:
        constraints = [models.UniqueConstraint("shop", "product", name="unique_product_in_shop")]
