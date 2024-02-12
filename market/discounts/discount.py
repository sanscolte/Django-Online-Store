from _decimal import Decimal
from typing import Tuple

from django.utils import timezone

from discounts.models import DiscountCart, DiscountProduct, DiscountSet
import cart.services
from products.models import Product
from shops.models import Offer


def calculate_set(products: list) -> Tuple[Decimal, int]:
    """Возвращает вес скидки и скидку на набор товаров"""

    discount_sets = DiscountSet.objects.filter(
        start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date()
    )
    flag = False
    for set in discount_sets:
        if set.is_active:
            for product in products:
                if product.category in set.categories.all():
                    weigth_set = set.weight
                    percentage_set = set.percentage
                    flag = True
                else:
                    break
    if not flag:
        weigth_set = 0
        percentage_set = 0
    return weigth_set, percentage_set


def calculate_cart(price: Decimal) -> Tuple[Decimal, int]:
    """Возвращает вес скидки и скидку на корзину"""

    carts = DiscountCart.objects.filter(start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date())
    weigth_cart = 0
    percentage_cart = 0
    for cart_discount in carts:
        if cart_discount.price_from <= price <= cart_discount.price_to and cart_discount.is_active:
            weigth_cart = cart_discount.weight
            percentage_cart = cart_discount.percentage
    return weigth_cart, percentage_cart


def calculate_products(price: Decimal, offer_product: Product, offer_price: Offer) -> Decimal:
    """Возвращает общую стоимость корзины с учетом скидки на товар"""

    discount_products = DiscountProduct.objects.filter(
        start_date__lte=timezone.now().date(), end_date__gte=timezone.now().date()
    )
    for product in discount_products:
        if offer_product in product.products.all():
            carts = cart.services.CartServices.cart
            quantity = carts[str(offer_product.pk)]["quantity"]
            price = price - ((offer_price * quantity) * product.percentage / 100)
    return price


def calculate_discount() -> Decimal:
    """Возвращает общую корзину с учетом всех скидок"""
    total_price = cart.services.CartServices.get_total_price()
    products = cart.services.CartServices.get_products_in_cart()
    offers = cart.services.CartServices.get_offers_in_cart()
    for offer in offers:
        total_price = calculate_products(total_price, offer.product, offer.price)
    weigth_cart, percentage_cart = calculate_cart(total_price)
    weigth_set, percentage_set = calculate_set(products)

    if weigth_set > weigth_cart:
        total_price = total_price - (total_price * percentage_set / 100)
    else:
        total_price = total_price - (total_price * percentage_cart / 100)
    return total_price
