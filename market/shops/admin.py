from django.contrib import admin
from .models import Shop, Offer


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = ("name",)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = "pk", "shop", "product", "price"
    list_display_links = ("pk",)
    ordering = "pk", "shop", "product"
    search_fields = "shop", "product"
