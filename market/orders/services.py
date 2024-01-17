from cart.services import CartServices


class OrderService:
    """Сервис для работы с заказами"""

    def __init__(self, request):
        self.request = request

    def get_total_price(self):
        """
        Получение стоимости заказа с учетом выбранного типа доставки
        :return: стоимость заказа
        """
        total_price = CartServices.get_total_price_with_discount()
        shops = CartServices.get_shops_in_cart()
        if self.request.session["delivery"] == "express":
            total_price += 500
        else:
            if total_price < 2000 or len(shops) > 1:
                total_price += 200
        return total_price
