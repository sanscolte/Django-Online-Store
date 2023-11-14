from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView


class ShopPageView(TemplateView):
    template_name = "shops/index.jinja2"
