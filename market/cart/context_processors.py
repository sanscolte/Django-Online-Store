from typing import Dict

from django.http import HttpRequest

from .services import CartServices


def cart_price(request: HttpRequest) -> Dict:
    "Взвращает данные для отбражения в бвзовом шаблоне"

    return {"cart_data": CartServices(request)}
