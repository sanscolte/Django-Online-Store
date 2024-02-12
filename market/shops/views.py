from django.db import ProgrammingError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect  # noqa F401
from django.conf import settings

from django.views.generic import TemplateView, View

from cart.forms import CartAddProductForm
from cart.services import CartServices
from discounts.models import DiscountProduct
from .models import Shop, Offer
from settings.models import SiteSetting

import random
from products.models import Banner, Product, Category


def get_products_list_cache_time() -> int:
    """Lazy-функция для получения времени действия кэша каталога продуктов"""

    try:
        timeout = SiteSetting.objects.first().product_list_cache_time
    except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
        timeout = settings.PRODUCT_LIST_CACHE_TIME
    return timeout


class IndexPageView(TemplateView):
    """Отоброжает главную страницу"""

    template_name = "shops/index.jinja2"

    def get_context_data(self, **kwargs):
        """Добавление баннеров и времени кэша в контекст шаблона"""

        context = super().get_context_data(**kwargs)
        context["discount_product"] = random.choice(DiscountProduct.objects.all())
        context["filtered_offers"] = Offer.objects.filter(remains__lte=50)
        context["cart_form"] = CartAddProductForm(initial={"quantity": 1, "update": False})
        context["categories"] = Category.objects.all()
        context["banners"] = random.choices(Banner.objects.filter(is_active=True), k=self.get_banners_count())
        context["banner_cache_time"] = self.get_banner_cache_time()
        context["show_days_offer"] = self.get_show_days_offer()
        context["top_items_count"] = self.get_top_items_count()
        context["limited_edition_count"] = self.get_limited_edition_count()
        return context

    def post(self, request: HttpRequest, **kwargs):
        cart_form = CartAddProductForm(request.POST)
        if cart_form.is_valid():
            product_name = request.POST["product_name"]
            product = Product.objects.get(name=product_name)
            offers = Offer.objects.all()
            for offer in offers:
                if offer.price == product.min_price[0] and offer.product.name == product.name:
                    shop = offer.shop
                    break
                else:
                    shop = None
            quantity = cart_form.cleaned_data["quantity"]
            cart_services = CartServices(request)
            cart_services.add(
                product=product,
                shop=shop,
                quantity=quantity,
                update_quantity=True,
            )
        return redirect("shops:home")

    def get_banner_cache_time(self) -> int:
        """Lazy-функция для получения времени действия кэша баннеров"""

        try:
            timeout = SiteSetting.objects.first().banner_cache_time
        except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
            timeout = settings.BANNER_CACHE_TIME
        return timeout

    def get_banners_count(self) -> int:
        """Lazy-функция для получения количества баннеров"""

        try:
            count = SiteSetting.objects.first().banners_count
        except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
            count = settings.BANNERS_COUNT
        return count

    def get_show_days_offer(self) -> bool:
        """Lazy-функция для получения значения отображения предложения дня"""

        try:
            days_offer = SiteSetting.objects.first().days_offer
        except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
            days_offer = settings.DAYS_OFFER
        return days_offer

    def get_top_items_count(self) -> int:
        """Lazy-функция для получения количества популярных товаров"""

        try:
            count = SiteSetting.objects.first().top_items_count
        except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
            count = settings.TOP_ITEMS_COUNT
        return count

    def get_limited_edition_count(self) -> int:
        """Lazy-функция для получения количества ограниченных тиражей"""

        try:
            count = SiteSetting.objects.first().limited_edition_count
        except (AttributeError, SiteSetting.DoesNotExist, ProgrammingError):
            count = settings.LIMITED_EDITION_COUNT
        return count


class ShopDetailView(View):
    """Отображает детальную страницу магазина"""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        shop = Shop.objects.get(pk=pk)
        offers = shop.offers.all()
        context = {
            "object": shop,
            "offers": offers,
        }
        return render(request, "shops/shops_detail.jinja2", context=context)
