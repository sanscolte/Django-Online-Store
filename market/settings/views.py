from django.core.cache import cache
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
            if "clear_all_cache" in request.POST:
                self.clear_all_cache()
            elif "clear_product_detail_cache" in self.request.POST:
                self.clear_cache_for_some_pages("product_detail")
            elif "clear_product_list_cache" in self.request.POST:
                self.clear_cache_for_some_pages("products")

        return self.get(request, context=settings_form, *args, **kwargs)

    def clear_all_cache(self):
        """Очистка кэша всего сайта"""

        cache.clear()

    def clear_cache_for_some_pages(self, part_key):
        """Очистка кэша для определённых страниц сайта"""

        keys_to_delete = [
            key[3:].decode("utf-8") for key in cache._cache.get_client().scan_iter(match=f"*{part_key}*")
        ]
        for key in keys_to_delete:
            cache.delete(key)

    def get_settings_dict(self):
        """Получение словаря настроек сайта"""

        temp_settings = SiteSetting.objects.first()
        settings_dict = {}
        for field in SiteSetting._meta.fields:
            settings_dict[field.name] = [getattr(temp_settings, field.name), str(type(field))]
        del settings_dict["id"], settings_dict["name"]
        return settings_dict
