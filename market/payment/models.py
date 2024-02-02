from django.db import models  # noqa

from orders.models import Order


class BankTransaction(models.Model):
    """Модель оплаты заказа"""

    class Meta:
        verbose_name = "Оплата заказа"
        verbose_name_plural = "Оплата заказов"

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=9)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_success = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.is_success} - {self.total_price} - {self.order.id} - {self.card_number}"
