from celery import shared_task
from payment.services import PaymentService


@shared_task
def pay(order_id, card_number, total_price):
    """Задача оплаты заказа"""
    payment = PaymentService(order_id, card_number, total_price)
    return payment.pay()
