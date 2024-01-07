from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from accounts.views import MyRegisterView
from orders.forms import OrderStepTwoForm


class OrderStepOneView(MyRegisterView):
    """
    Отображает страницу первого шага заказа
    """

    template_name = "orders/order_step_1.jinja2"
    success_url = reverse_lazy("orders:order_step_2")

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("orders:order_step_2"))
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
        return reverse("orders:order_step_3")
