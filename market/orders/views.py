from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpRequest
from django.views.generic import TemplateView, ListView, DetailView

from accounts.views import MyRegisterView
from orders.forms import OrderStepTwoForm, OrderStepThreeForm
from orders.models import Order, OrderItem
from shops.models import Offer
from orders.services import OrderService
from cart.services import CartServices
from products.models import ProductImage


class OrderStepOneView(MyRegisterView):
    """
    Отображает страницу первого шага заказа
    """

    template_name = "orders/order_step_1.jinja2"
    success_url = reverse_lazy("orders:order-step-2")

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("orders:order-step-2"))
        return super().post(request, *args, **kwargs)


class OrderStepTwoView(LoginRequiredMixin, FormView):
    """
    Отображает страницу второго шага заказа
    """

    form_class = OrderStepTwoForm
    template_name = "orders/order_step_2.jinja2"
    login_url = "/login/"

    def form_valid(self, form):
        self.request.session["delivery"] = form.cleaned_data["delivery_type"]
        self.request.session["city"] = form.cleaned_data["city"]
        self.request.session["address"] = form.cleaned_data["address"]
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.session.get("delivery"):
            initial["delivery_type"] = self.request.session.get("delivery")
        if self.request.session.get("city"):
            initial["city"] = self.request.session.get("city")
        if self.request.session.get("address"):
            initial["address"] = self.request.session.get("address")
        return initial

    def get_success_url(self):
        return reverse("orders:order-step-3")


class OrderStepThreeView(LoginRequiredMixin, FormView):
    """
    Отображает страницу третьего шага заказа
    """

    form_class = OrderStepThreeForm
    template_name = "orders/order_step_3.jinja2"
    login_url = "/login/"

    def form_valid(self, form):
        self.request.session["payment"] = form.cleaned_data["payment_type"]
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.session.get("payment"):
            initial["payment_type"] = self.request.session.get("payment")
        return initial

    def get_success_url(self):
        return reverse("orders:order-step-4")


class OrderStepFourView(LoginRequiredMixin, TemplateView):
    """
    Отображает страницу четвертого шага заказа
    """

    template_name = "orders/order_step_4.jinja2"

    def post(self, request, *args, **kwargs):
        cart = CartServices(self.request)
        order_service = OrderService(self.request)
        order = Order.objects.create(
            phone_number=request.user.phone_number,
            full_name=request.user.full_name,
            email=request.user.email,
            delivery_type=request.session["delivery"],
            city=request.session["city"],
            address=request.session["address"],
            payment_type=request.session["payment"],
            total_price=order_service.get_total_price(),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                offer=Offer.objects.get(id=int(item["offers"])),
                price=item["price"],
                quantity=item["quantity"],
            )
        if request.session["payment"] == "card":
            url = reverse("payment:payment_with_card")
            return HttpResponseRedirect(f"{url}?order={order.pk}&total_price={order.total_price}")

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_service = OrderService(self.request)
        cart = CartServices(self.request)
        context["cart"] = cart
        for item in cart:
            item["images"] = ProductImage.objects.filter(product=item["product"].pk)
        context["delivery"] = self.request.session["delivery"]
        context["city"] = self.request.session["city"]
        context["address"] = self.request.session["address"]
        context["payment"] = self.request.session["payment"]
        context["total_price"] = order_service.get_total_price()
        return context


class HistoryOrderListView(ListView, LoginRequiredMixin):
    """Страница списка заказов"""

    template_name = "orders/history_order.jinja2"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(email=self.request.user.email).order_by("-pk")


class HistoryOrderDetailView(DetailView, LoginRequiredMixin):
    """Детальная страница заказа"""

    template_name = "orders/order_detail.jinja2"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(email=self.request.user.email)
