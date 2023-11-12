from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Категория"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"), unique=True)
    description = models.TextField(verbose_name=_("описание"), blank=True)
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_index = models.CharField(verbose_name=_("индекс сортировки"), blank=True)

    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    """Продукт"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    description = models.TextField(verbose_name=_("описание"), blank=True)
    number_of_purchases = models.IntegerField(default=0)
    date_of_publication = models.DateField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))

    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"{self.name}"


class Detail(models.Model):
    """Свойство продукта"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))


class ProductDetail(models.Model):
    """Значение свойства продукта"""

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name=_("характеристика"))
    value = models.CharField(max_length=128, verbose_name=_("значение"))

    class Meta:
        constraints = [models.UniqueConstraint("product", "detail", name="unique_detail_for_product")]


class ProductImage(models.Model):
    """Фотографии продукта"""

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_("изображение"), blank=True)
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
