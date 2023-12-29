from typing import List, Dict

from psycopg2._psycopg import Decimal

from discounts.models import DiscountCart, DiscountProduct, DiscountSet
from shops.models import Offer


def calculate_discount(offers: List[Dict[Offer, int]]):
    total_price = Decimal("0")
    products = []
    carts = DiscountCart.objects.all()
    discount_products = DiscountProduct.objects.all()
    discount_sets = DiscountSet.objects.all()
    for offer in offers:
        for offer_obj, quantity in offer.items():
            products += [offer_obj.product.name] * quantity
            total_price += offer_obj.price * quantity
    for product in discount_products:
        if product.name in products:
            total_price = total_price - (total_price * product.percentage)
    for set in discount_sets:
        if set.is_active:
            weigth_set = set.weigth
            percentage_set = set.percentage
    for cart in carts:
        if cart.price_from <= total_price <= cart.price_to and cart.is_active:
            weigth_cart = cart.weigth
            percentage_cart = cart.percentage
    if weigth_set > weigth_cart:
        total_price = total_price - total_price * percentage_cart
    else:
        total_price = total_price - total_price * percentage_set
    return total_price
