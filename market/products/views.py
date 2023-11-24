from django.shortcuts import render  # noqa F401

from django.views.generic import ListView
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from products.models import Product
from .constants import KEY_FOR_CACHE_PRODUCTS


@method_decorator(cache_page(60 * 5, key_prefix=KEY_FOR_CACHE_PRODUCTS), name="dispatch")
class ProductListView(ListView):
    template_name = "products/catalog.jinja2"
    context_object_name = "products"
    model = Product
    paginate_by = settings.PAGINATE_PRODUCTS_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get("sort_by")

        if sort_by == "date_of_publication":
            queryset = queryset.order_by("-date_of_publication")
        if sort_by == "price":
            queryset = queryset.order_by("offers.products")

        return queryset
