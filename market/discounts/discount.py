from typing import List, Dict

from psycopg2._psycopg import Decimal

from shops.models import Offer


def calculate_discount(offers: List[Dict[Offer, int]]):
    total_price = Decimal("0")
    products = []

    for offer in offers:
        for offer_obj, quantity in offer.items():
            products += [offer_obj.product.name] * quantity
            total_price += offer_obj.price * quantity

    return 0
