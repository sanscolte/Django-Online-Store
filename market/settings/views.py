from django.core.cache import cache
from django.http import HttpRequest
from django.views.generic import ListView

from settings.forms import SettingsForm, ClearCacheForm
from settings.models import SiteSetting


class SettingsView(ListView):
    """Представление настроек сайта"""

    model = SiteSetting
    template_name = "settings/settings.jinja2"
    context_object_name = "setting"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings_dict"] = self.get_settings_dict()
        context["user"] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        current_settings = SiteSetting.objects.first()

        settings_form = SettingsForm(request.POST, instance=current_settings)
        clear_cache_form = ClearCacheForm(request.POST)

        if settings_form.is_valid():
            settings_form.save()

        if clear_cache_form.is_valid():
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

    def clear_cache_for_some_pages(self, part_key: str) -> None:
        """Функция для очистки кэша определённых страниц сайта по части ключа кэша"""

        keys_to_delete = [
            key[3:].decode("utf-8") for key in cache._cache.get_client().scan_iter(match=f"*{part_key}*")
        ]
        for key in keys_to_delete:
            cache.delete(key)

    def get_settings_dict(self) -> dict:
        """Функция для получения словаря настроек сайта"""

        temp_settings = SiteSetting.objects.first()
        settings_dict = {}
        for field in SiteSetting._meta.fields:
            settings_dict[field.name] = [getattr(temp_settings, field.name), str(type(field))]
        del settings_dict["id"], settings_dict["name"]
        return settings_dict
