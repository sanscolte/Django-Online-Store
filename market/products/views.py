from django.shortcuts import render  # noqa F401

from django.views.generic import ListView
from django.conf import settings
from products.models import Product


class ProductListView(ListView):
    template_name = "products/catalog.jinja2"
    model = Product
    context_object_name = "products"
    paginate_by = settings.PAGINATE_PRODUCTS_BY
