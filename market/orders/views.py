from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from accounts.views import MyRegisterView


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
