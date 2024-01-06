from django.db import models
from products.models import Product


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

    full_name = models.CharField(max_length=50, verbose_name="full name")
    email = models.EmailField(verbose_name="email")
    phone_number = models.CharField(max_length=12, unique=True, verbose_name="phone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    delivery_type = models.CharField(
        max_length=50,
        choices=DeliveryTypes.choices,
        verbose_name="delivery type",
        blank=False,
        default=DeliveryTypes.REGULAR,
    )
    address = models.CharField(max_length=250, verbose_name="address")
    city = models.CharField(max_length=50, verbose_name="city")
    payment_type = models.CharField(
        max_length=50,
        choices=PaymentTypes.choices,
        blank=False,
        default=PaymentTypes.CARD,
        verbose_name="payment type",
    )
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.STATUS_CREATED, verbose_name="status"
    )


class OrderItem(models.Model):
    """Модель заказов с продуктами"""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
