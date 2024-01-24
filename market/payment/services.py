class PaymentService:
    """Сервис оплаты заказа"""

    def __init__(self, order_id, card_number, total_price):
        self.order_id = order_id
        self.card_number = str(card_number)
        self.total_price = total_price

    def pay(self):
        ...
