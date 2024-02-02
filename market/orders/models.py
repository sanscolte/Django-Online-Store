from django.db import models
from shops.models import Offer
from django.utils.translation import gettext_lazy as _


class DeliveryTypes(models.TextChoices):
    """Модель выбора типа доставки"""

    REGULAR = "regular", "обычная доставка"
    EXPRESS = "express", "экспресс-доставка"


class PaymentTypes(models.TextChoices):
    """Модель выбора типа оплаты"""

    CARD = "card", "онлайн картой"
    RANDOM = "random", "онлайн со случайного чужого счета"


class Status(models.TextChoices):
    """Модель выбора статуса заказа"""

    STATUS_CREATED = "created"
    STATUS_OK = "ok"
    STATUS_DELIVERED = "delivered"
    STATUS_PAID = "paid"
    STATUS_NOT_PAID = "not paid"


class Order(models.Model):
    """Модель заказа с информацией о пользователе"""

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")

    full_name = models.CharField(max_length=50, verbose_name=_("полное имя"))
    email = models.EmailField(verbose_name=_("email"))
    phone_number = models.CharField(max_length=12, verbose_name=_("телефон"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("создан"))
    delivery_type = models.CharField(
        max_length=50,
        choices=DeliveryTypes.choices,
        verbose_name=_("доставка"),
        blank=False,
        default=DeliveryTypes.REGULAR,
    )
    address = models.CharField(max_length=250, verbose_name=_("адрес"))
    city = models.CharField(max_length=50, verbose_name=_("город"))
    payment_type = models.CharField(
        max_length=50,
        choices=PaymentTypes.choices,
        blank=False,
        default=PaymentTypes.CARD,
        verbose_name=_("оплата"),
    )
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.STATUS_CREATED, verbose_name=_("статус")
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_("итоговая цена"))


class OrderItem(models.Model):
    """Модель заказов с продуктами"""

    class Meta:
        verbose_name = _("Продукты в Заказе")
        verbose_name_plural = _("Продукты в Заказе")

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name=_("заказ"))
    offer = models.ForeignKey(
        Offer, related_name="order_items", on_delete=models.CASCADE, verbose_name=_("предложение")
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("количество"))
