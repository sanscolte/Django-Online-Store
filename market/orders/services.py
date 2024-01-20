from _decimal import Decimal

from django.http import HttpRequest

from cart.services import CartServices
from .constants import standard_order_price, express_order_price


class OrderService:
    """Сервис для работы с заказами"""

    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def get_total_price(self) -> Decimal:
        """
        Получение стоимости заказа с учетом выбранного типа доставки
        :return: стоимость заказа
        """
        total_price = CartServices.get_total_price_with_discount()
        shops = CartServices.get_shops_in_cart()
        if self.request.session["delivery"] == "express":
            total_price += express_order_price
        else:
            if total_price < 2000 or len(shops) > 1:
                total_price += standard_order_price
        return total_price
