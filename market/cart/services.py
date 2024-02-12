from decimal import Decimal

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest

from products.models import Product
from shops.models import Shop, Offer
from discounts.discount import calculate_discount
import random


class CartServices:
    _instance = None

    def __new__(cls, request: HttpRequest, *args, **kwargs):
        """Создает корзину"""

        cls.session: SessionBase = request.session
        cart = cls.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = cls.session[settings.CART_SESSION_ID] = {}
        cls.cart = cart
        if not CartServices._instance:
            CartServices._instance = super(CartServices, cls).__new__(cls, *args, **kwargs)

        return CartServices._instance

    def add(self, product: Product, shop: None, quantity=1, update_quantity=False) -> None:
        """Добавление товара в корзину или обновление его количества."""

        if not shop:
            shops = Shop.objects.filter(products=product)
            shop = random.choice(shops)
        product_id = str(product.id)
        offer = Offer.objects.get(product=product, shop__name=shop)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(offer.price), "offers": str(offer.id)}
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
        """Проходим по товарам корзины и получаем соответствующие объекты.
        :return: dict
        quantity: количество товра
        price: цена за единицу товра
        offers: id предлжения
        product: товар
        price: общая цена за единицу товра
        update_quantity_form: форма для обновления товара
        """

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

    @classmethod
    def get_total_price(cls) -> Decimal:
        """Возвращает общую стоимость товаров в корзине."""

        total_price = sum(Decimal(item["price"]) * item["quantity"] for item in cls.cart.values())

        return total_price

    @classmethod
    def get_total_price_with_discount(cls) -> Decimal:
        """Возвращает общую стоимость товаров в корзине c учетом скидки."""

        total_price = calculate_discount()

        return total_price

    @classmethod
    def get_products_in_cart(cls) -> list:
        """Возвращает список экземпляров модели Product корзины."""

        product_ids = cls.cart.keys()
        products_in_cart = Product.objects.filter(id__in=product_ids)
        return products_in_cart

    @classmethod
    def get_offers_in_cart(cls) -> list:
        """Возвращает список экземпляров модели Offer корзины."""

        offer_ids = (item["offers"] for item in cls.cart.values())
        offers_in_cart = Offer.objects.filter(id__in=offer_ids)
        return offers_in_cart

    @classmethod
    def get_shops_in_cart(cls) -> list:
        """Возвращает список магазинов корзины."""

        offer_ids = (item["offers"] for item in cls.cart.values())
        offers_in_cart = Offer.objects.filter(id__in=offer_ids)
        shops_in_cart = []
        for item in offers_in_cart:
            if item.shop not in shops_in_cart:
                shops_in_cart.append(item.shop)
        return shops_in_cart

    def clear(self) -> None:
        """Очистка корзины."""

        self.cart = {}
        self.save()
