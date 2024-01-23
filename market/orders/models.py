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

    full_name = models.CharField(max_length=50, verbose_name="полное имя")
    email = models.EmailField(verbose_name="email")
    phone_number = models.CharField(max_length=12, verbose_name="телефон")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    delivery_type = models.CharField(
        max_length=50,
        choices=DeliveryTypes.choices,
        verbose_name="доставка",
        blank=False,
        default=DeliveryTypes.REGULAR,
    )
    address = models.CharField(max_length=250, verbose_name="адрес")
    city = models.CharField(max_length=50, verbose_name="город")
    payment_type = models.CharField(
        max_length=50,
        choices=PaymentTypes.choices,
        blank=False,
        default=PaymentTypes.CARD,
        verbose_name="оплата",
    )
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.STATUS_CREATED, verbose_name="статус"
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="итоговая цена")

    # TODO реализовать строковое представление и class meta для определения verbose и verbose_plural к модели


class OrderItem(models.Model):
    """Модель заказов с продуктами"""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="заказ")
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE, verbose_name="продукт")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="количество")

    # TODO реализовать строковое представление и class meta для определения verbose и verbose_plural к модели
