from django.views.generic import ListView, DetailView

from django.conf import settings

from discounts.models import DiscountProduct, DiscountSet, DiscountCart


class DiscountListView(ListView):
    """Страница списка всех скидок"""

    template_name = "discounts/discounts_list.jinja2"
    model = DiscountProduct
    context_object_name = "discounts"
    paginate_by = settings.PAGINATE_PRODUCTS_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discount_sets = DiscountSet.objects.all().order_by("-weight")
        discount_carts = DiscountCart.objects.all().order_by("-weight")
        context["discount_sets"] = discount_sets
        context["discount_carts"] = discount_carts
        return context


class DiscountProductDetailView(DetailView):
    """Детальная страница скидки продукта"""

    template_name = "discounts/discount-product.jinja2"
    model = DiscountProduct
    context_object_name = "discount_product"


class DiscountCartDetailView(DetailView):
    """Детальная страница скидки корзины"""

    template_name = "discounts/discount-cart.jinja2"
    model = DiscountCart
    context_object_name = "discount_cart"


class DiscountSetDetailView(DetailView):
    """Детальная страница скидки набора"""

    template_name = "discounts/discount-sets.jinja2"
    model = DiscountSet
    context_object_name = "discount_set"
