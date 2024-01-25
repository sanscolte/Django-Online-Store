from django import forms
from .models import SiteSetting


class SettingsForm(forms.ModelForm):
    """Форма настроек сайта"""

    class Meta:
        model = SiteSetting
        fields = [
            "min_order_price_for_free_shipping",
            "standard_order_price",
            "express_order_price",
            "banners_count",
            "days_offer",
            "top_items_count",
            "limited_edition_count",
            "product_cache_time",
            "banner_cache_time",
            "product_list_cache_time",
        ]


class ClearCacheForm(forms.Form):
    """Форма очистки кэша сайта"""

    clear_all_cache = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    clear_product_detail_cache = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    clear_product_list_cache = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
