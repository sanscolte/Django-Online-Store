from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView, DetailView
from .models import Shop


class ShopPageView(TemplateView):
    template_name = "shops/index.jinja2"


class ShopDetailView(DetailView):
    template_name = "shops/shops_detail.jinja2"
    queryset = Shop.objects.prefetch_related("products")
