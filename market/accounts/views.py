from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from django.views.generic import TemplateView
from .forms import UserLoginForm


class MyAccountView(TemplateView):
    pass


class MyLoginView(LoginView):
    template_name = "accounts/login.jinja2"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.POST.get("next"):
            next_page = self.request.POST.get("next")
        else:
            next_page = reverse("shops:home")
        return next_page
