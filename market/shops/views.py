from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView, ListView

from config.settings import Paginate
from products.models import Product


class ShopPageView(TemplateView):
    template_name = "shops/index.jinja2"


class ProductListView(ListView):
    template_name = "shops/catalog.jinja2"
    model = Product
    context_object_name = "products"
    paginate_by = Paginate
