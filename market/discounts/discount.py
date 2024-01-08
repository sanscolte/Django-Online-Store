from typing import List, Dict

from psycopg2._psycopg import Decimal

from discounts.models import DiscountCart, DiscountProduct, DiscountSet
from shops.models import Offer


def calculate_set(products):
    flag = True
    discount_sets = DiscountSet.objects.all()
    for set in discount_sets:
        if set.is_active:
            for product in products:
                if product.category in set.categories.all():
                    weigth_set = set.weigth
                    percentage_set = set.percentage
                    flag = True
                else:
                    flag = False
                    break
    if not flag:
        weigth_set = 0
        percentage_set = 0
    return percentage_set, weigth_set


def calculate_cart(price):
    carts = DiscountCart.objects.all()
    for cart in carts:
        if cart.price_from <= price <= cart.price_to and cart.is_active:
            weigth_cart = cart.weigth
            percentage_cart = cart.percentage
    return weigth_cart, percentage_cart


def calculate_products(price, products):
    discount_products = DiscountProduct.objects.all()
    for product in discount_products:
        if product.name in products:
            price = price - (price * product.percentage)
    return price


def calculate_discount(offers: List[Dict[Offer, int]]):
    total_price = Decimal("0")
    products = []
    for offer in offers:
        for offer_obj, quantity in offer.items():
            products += [offer_obj.product.name] * quantity
            total_price += offer_obj.price * quantity
    total_price = calculate_products(total_price, products)
    weigth_cart, percentage_cart = calculate_cart(total_price)
    weigth_set, percentage_set = calculate_set(products)

    if weigth_set > weigth_cart:
        total_price = total_price - (total_price * percentage_cart)
    else:
        total_price = total_price - (total_price * percentage_set)
    return total_price
