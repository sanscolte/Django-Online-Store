from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin


class MyRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = ""
    success_url = reverse_lazy("account:my-account")


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
        previous_page = self.request.GET.get("next") if self.request.GET.get("next") is not None else "/"
        next_page = previous_page
        return next_page


class MyLogoutView(LogoutView):
    """Класс представления для выхода пользователя"""

    next_page = reverse_lazy("shops:home")
