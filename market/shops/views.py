from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect  # noqa F401
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView, View

from cart.forms import CartAddProductForm
from cart.services import CartServices
from discounts.models import DiscountProduct
from products.constants import KEY_FOR_CACHE_PRODUCTS
from .models import Shop, Offer
from settings.models import SiteSetting

import random
from products.models import Banner, Product, Category


@method_decorator(cache_page(60 * 5, key_prefix=KEY_FOR_CACHE_PRODUCTS), name="dispatch")
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
        except ValueError:
            timeout = 600
        return timeout

    def get_banners_count(self) -> int:
        """Lazy-функция для получения количества баннеров"""

        try:
            count = SiteSetting.objects.first().banners_count
        except ValueError:
            count = 3
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
