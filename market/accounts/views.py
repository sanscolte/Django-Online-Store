from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from .forms import UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin


class MyAccountView(LoginRequiredMixin, TemplateView):
    """Личный кабинет пользователя"""

    template_name = "accounts/my-account.jinja2"
    login_url = "/login/"


class MyLoginView(LoginView):
    """Класс представления для входа пользователя"""

    template_name = "accounts/login.jinja2"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.POST.get("next"):
            next_page = self.request.POST.get("next")
        else:
            next_page = reverse("shops:home")
        return next_page


class MyLogoutView(LogoutView):
    """Класс представления для выхода пользователя"""

    next_page = reverse_lazy("shops:home")
