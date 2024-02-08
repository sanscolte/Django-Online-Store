import os
import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from .constants import KEY_FOR_CACHE_PRODUCTS
from django.core.cache import cache
from django.db.models import signals


def save_product(**kwargs):
    """Удаление кэша при получении сигнала об изменении или создании продукта"""
    cache.delete(KEY_FOR_CACHE_PRODUCTS)


def delete_product(**kwargs):
    """Удаление кэша при получении сигнала об удалении продукта"""
    cache.delete(KEY_FOR_CACHE_PRODUCTS)


class Category(models.Model):
    """Модель категории товара"""

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

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
    """Модель продукта"""

    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    description = models.TextField(verbose_name=_("описание"), blank=True)
    date_of_publication = models.DateTimeField(default=timezone.now)
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

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("products:product-detail", kwargs={"pk": self.pk})


signals.post_save.connect(receiver=save_product, sender=Product)
signals.post_delete.connect(receiver=delete_product, sender=Product)


class Detail(models.Model):
    """Модель характеристики продукта"""

    name = models.CharField(max_length=512, verbose_name=_("наименование"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Характеристика")
        verbose_name_plural = _("Характеристики")


class ProductDetail(models.Model):
    """Модель значения характеристики продукта"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name=_("характеристика"), default=0)
    value = models.CharField(max_length=128, verbose_name=_("значение"))

    def __str__(self) -> str:
        return f"{self.detail.name} товара {self.product.name}"

    class Meta:
        constraints = [models.UniqueConstraint("product", "detail", name="unique_detail_for_product")]
        verbose_name = _("Характеристика продукта")
        verbose_name_plural = _("Характеристики продукта")


def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    """Функция создания уникального пути к изображениям продукта"""

    return "products/{product}/{filename}".format(
        product=instance.product.name,
        filename=filename,
    )


class ProductImage(models.Model):
    """Модель фотографий продукта"""

    class Meta:
        verbose_name = _("Фотография продукта")
        verbose_name_plural = _("Фотографии продуктов")

    def __str__(self) -> str:
        return f"Фотографии товара {self.product.name}"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to=product_image_directory_path, verbose_name=_("изображение"), default=1)
    sort_image = models.IntegerField()


def banner_preview_directory_path(instance: "Banner", filename: str) -> str:
    """Функция создания уникального пути к баннеру"""

    """
    Функция создания уникального пути к баннеру
    :param instance: Баннер
    :param filename: Имя файла
    :return: путь до файла
    """
    return "banners/{product}/{filename}".format(
        product=instance.product.name,
        filename=filename,
    )


class Banner(models.Model):
    """Модель баннера"""

    class Meta:
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="banners")
    image = models.ImageField(upload_to=banner_preview_directory_path, verbose_name=_("изображение"))
    is_active = models.BooleanField(default=True)


class Review(models.Model):
    """Модель отзыва"""

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self) -> str:
        return f"{self.user} ({self.created_at}): {self.text}"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name=_("Продукт"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    text = models.TextField(blank=True, max_length=3000, verbose_name=_("Отзыв"))
    created_at = models.DateTimeField(default=timezone.now)


class ProductsViews(models.Model):
    """Модель истории просмотров продуктов"""

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "История просмотра"
        verbose_name_plural = "История просмотров"

    def __str__(self) -> str:
        return f"{self.user} ({self.created_at}): {self.product}"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products_views", verbose_name=_("Пользователь")
    )  # noqa
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products_views", verbose_name=_("Продукт")
    )
    created_at = models.DateTimeField(default=timezone.now)


class ComparisonList(models.Model):
    """Модель списка сравнения продуктов"""

    anonymous_user = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name="comparison_list", blank=True)

    class Meta:
        verbose_name = _("Список сравнения")
        verbose_name_plural = _("Списки сравнения")

    def __str__(self) -> str:
        return f"Список сравнения пользователя {self.user.name}"


class ProductImport(models.Model):
    """Модель хранения файла импорта продукта"""

    class Meta:
        verbose_name = "Импорт продукта"
        verbose_name_plural = "Импорт продуктов"

    file = models.FileField(upload_to="import/")

    def save(self, *args, **kwargs):
        """Сохраняем файл с рандомной строчкой в начале"""
        if not self.pk:
            unique_filename = str(uuid.uuid4()) + "_" + self.file.name
            self.file.name = os.path.join(unique_filename)
        super(ProductImport, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.file}"
