from decimal import Decimal

from django.conf import settings
from products.models import Product
from shops.models import Shop, Offer
import random


class CartServices:
    def __init__(self, request):
        """Создает корзину"""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, shop: None, quantity=1, update_quantity=False) -> None:
        """Добавление товара в корзину или обновление его количества."""

        if not shop:
            shops = Shop.objects.filter(products=product)
            shop = random.choice(shops)
        product_id = str(product.id)
        offer = Offer.objects.get(product=product, shop__name=shop)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(offer.price)}
        if update_quantity:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id]["quantity"] = quantity
        self.save()

    def save(self) -> None:
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product: Product) -> None:
        """Удаление товара из корзины."""

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты."""

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self) -> int:
        """Возвращает общее количество товаров в корзине."""

        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        """Возвращает общую стоимость товаров в корзине."""

        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self, only_session: bool = False) -> None:
        """Очистка корзины."""

        del self.session[settings.CART_SESSION_ID]
        self.save()
