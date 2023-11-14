import random

from django.shortcuts import render  # noqa F401
from django.views.generic import TemplateView

from products.models import Banner


class ShopPageView(TemplateView):
    template_name = "shops/index.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banners"] = random.choices(Banner.objects.filter(is_active=True), k=3)
        return context
