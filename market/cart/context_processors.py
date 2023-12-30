from .services import CartServices


def cart_price(request):
    "Взвращает данные для отбражения в бвзовом шаблоне"

    return {"cart_data": CartServices(request)}
