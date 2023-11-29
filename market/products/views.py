from django.db.models import Avg
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
    paginate_by = settings.PAGINATE_PRODUCTS_BY

    def get_queryset(self):
        queryset = (
            Product.objects.annotate(avg_price=Avg("offers__price"))
            .filter(avg_price__range=(1_000, 1_000_000))
            .order_by("-avg_price")
        )
        sort_by = self.request.GET.get("sort_by")

        if sort_by == "date_of_publication":
            queryset = queryset.order_by("-date_of_publication")
        if sort_by == "price":
            queryset = queryset.order_by("avg_price")
        return queryset
