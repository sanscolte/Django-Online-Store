from django.http import HttpRequest, HttpResponse
from django.shortcuts import render  # noqa F401

from django.views.generic import TemplateView, ListView, View

from django.conf import settings
from products.models import Product

from .models import Shop


class ShopPageView(TemplateView):
    template_name = "shops/index.jinja2"


class ProductListView(ListView):
    template_name = "shops/catalog.jinja2"
    model = Product
    context_object_name = "products"
    paginate_by = settings.PAGINATE_PRODUCTS_BY


class ShopDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        shop = Shop.objects.get(pk=pk)
        offers = shop.offers.all()
        context = {
            "object": shop,
            "offers": offers,
        }
        return render(request, "shops/shops_detail.jinja2", context=context)
