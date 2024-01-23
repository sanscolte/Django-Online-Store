from django.http import HttpRequest, HttpResponse
from django.shortcuts import render  # noqa F401

from django.views.generic import TemplateView, View

from settings.models import SiteSetting
from .models import Shop

import random
from products.models import Banner, Category


class IndexPageView(TemplateView):
    template_name = "shops/index.jinja2"

    def get_context_data(self, **kwargs):
        """Добавление баннеров и времени кэша в контекст шаблона"""

        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["banners"] = random.choices(
            Banner.objects.filter(is_active=True), k=SiteSetting.objects.first().banners_count
        )
        context["banner_cache_time"] = SiteSetting.objects.first().banner_cache_time
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
