from celery import shared_task

from payment.models import BankTransaction
from payment.services import PaymentService


@shared_task
def pay():
    """Задача оплаты заказа, проверяет модели со статусом None"""

    for transaction in BankTransaction.objects.filter(is_success=None):
        payment = PaymentService(transaction.order, transaction.card_number, transaction.total_price, transaction)
        payment.pay()
