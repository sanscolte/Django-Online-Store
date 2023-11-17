from django.http import HttpRequest, HttpResponse
from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView, View
from .models import Shop


class ShopPageView(TemplateView):
    template_name = "shops/index.jinja2"


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
