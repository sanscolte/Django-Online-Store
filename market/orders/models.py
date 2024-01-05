from django.db import models
from products.models import Product


class Order(models.Model):
    """Модель заказа с информацией о пользователе"""

    DELIVERY_TYPES = [("regular", "обычная доставка"), ("express", "экспресс-доставка")]

    PAYMENT_TYPES = [("card", "онлайн картой"), ("random", "онлайн со случайного чужого счета")]

    STATUS_CREATED = "created"
    STATUS_OK = "ok"
    STATUS_DELIVERED = "delivered"
    STATUS_PAID = "paid"
    STATUS_NOT_PAID = "not paid"
    STATUS_CHOICES = [
        (
            "Success",
            (
                (STATUS_CREATED, "создан"),
                (STATUS_OK, "выполнен"),
                (STATUS_DELIVERED, "доставляется"),
                (STATUS_PAID, "оплачен"),
            ),
        ),
        (STATUS_NOT_PAID, "не оплачен"),
    ]

    full_name = models.CharField(max_length=50, verbose_name="full name")
    email = models.EmailField(verbose_name="email")
    phone_number = models.CharField(max_length=12, unique=True, verbose_name="phone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    delivery_type = models.CharField(
        max_length=50, choices=DELIVERY_TYPES, verbose_name="delivery type", blank=False, default=DELIVERY_TYPES[0]
    )
    address = models.CharField(max_length=250, verbose_name="address")
    city = models.CharField(max_length=50, verbose_name="city")
    payment_type = models.CharField(
        max_length=50, choices=PAYMENT_TYPES, blank=False, default=PAYMENT_TYPES[0], verbose_name="payment type"
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name="status")


class OrderItem(models.Model):
    """Модель заказов с продуктами"""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
