from django.views.generic import TemplateView


class DiscountTemplateView(TemplateView):
    template_name = "products/discount_products.jinja2"
