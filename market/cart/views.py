from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from cart.forms import CartAddProductForm
from cart.services import CartServices
from products.models import Product


class CartDetail(TemplateView):
    template_name = "cart/details.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartServices(self.request)
        context["cart"] = cart
        for item in cart:
            item["update_quantity_form"] = CartAddProductForm(initial={"quantity": item["quantity"], "update": False})
        return context


@require_POST
def cart_add(request: HttpRequest, pk: int) -> HttpResponse:
    """Добавление товара в корзину"""

    cart = CartServices(request)
    product = get_object_or_404(Product, id=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, shop=None, quantity=cd["quantity"], update_quantity=cd["update"])
    return redirect("cart:cart_detail")


def cart_remove(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаление товара в корзины"""

    cart = CartServices(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect("cart:cart_detail")
