from django.core.cache import cache
from django.http import HttpRequest
from django.views.generic import ListView
from django.contrib import messages

from settings.forms import SettingsForm, ClearCacheForm
from settings.models import SiteSetting


class SettingsView(ListView):
    """Представление настроек сайта"""

    model = SiteSetting
    template_name = "settings/settings.jinja2"
    context_object_name = "setting"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        settings_form = SettingsForm(instance=SiteSetting.objects.first())
        context["settings_form"] = settings_form

        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        current_settings = SiteSetting.objects.first()

        settings_form = SettingsForm(request.POST, instance=current_settings)
        clear_cache_form = ClearCacheForm(request.POST)

        action_cache = False
        for key in request.POST:
            if key.startswith("clear") and key.endswith("cache"):
                action_cache = True
                break

        if settings_form.is_valid():
            cache.clear()
            settings_form.save()
            messages.success(request, "Настройки успешно сохранены.")
        elif not settings_form.is_valid() and not action_cache:
            error_messages = []
            for field, errors in settings_form.errors.items():
                error_messages.append(f"{field}: {', '.join(errors)}")
            error_message = "\n".join(error_messages)
            messages.error(request, "Пожалуйста, исправьте ошибки в форме настроек.")
            messages.error(request, error_message)
        elif clear_cache_form.is_valid():
            self.handle_cache_clear(request, clear_cache_form)

        return self.get(request, context=settings_form, *args, **kwargs)

    def handle_cache_clear(self, request: HttpRequest, clear_cache_form: "ClearCacheForm") -> None:
        """Функция для обработки формы очистки кэша"""

        if clear_cache_form.cleaned_data.get("clear_all_cache"):
            self.clear_all_cache()
        elif clear_cache_form.cleaned_data.get("clear_product_detail_cache"):
            self.clear_cache_for_some_pages("product_detail")
        elif clear_cache_form.cleaned_data.get("clear_product_list_cache"):
            self.clear_cache_for_some_pages("products")

    def clear_all_cache(self) -> None:
        """Функция для очистки кэша всего сайта"""

        cache.clear()
        messages.success(self.request, "Кэш всего сайта успешно очищен.")

    def clear_cache_for_some_pages(self, part_key: str) -> None:
        """Функция для очистки кэша определённых страниц сайта по части ключа кэша"""

        keys_to_delete = [
            key[3:].decode("utf-8") for key in cache._cache.get_client().scan_iter(match=f"*{part_key}*")
        ]
        for key in keys_to_delete:
            cache.delete(key)
        messages.success(self.request, "Кэш отдельных страниц успешно очищен.")
