from django.http import HttpRequest, HttpResponse
from django.shortcuts import render  # noqa F401

from django.views.generic import TemplateView, View

from .models import Shop

import random
from config.settings import CACHE_TIME
from products.models import Banner


class IndexPageView(TemplateView):
    template_name = "shops/index.jinja2"

    def get_context_data(self, **kwargs):
        """Добавление баннеров и времени кэша в контекст шаблона"""

        context = super().get_context_data(**kwargs)
        context["banners"] = random.choices(Banner.objects.filter(is_active=True), k=3)
        context["cache_time"] = CACHE_TIME
        return context


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
