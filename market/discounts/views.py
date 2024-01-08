from django.views.generic import ListView

from django.conf import settings

from discounts.models import DiscountProduct


class DiscountTemplateView(ListView):
    template_name = "discounts/discounts_list.jinja2"
    model = DiscountProduct
    context_object_name = "discounts"
    paginate_by = settings.PAGINATE_PRODUCTS_BY
