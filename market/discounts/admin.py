from django.contrib import admin

from discounts.models import DiscountSet, DiscountProduct, DiscountCart


@admin.register(DiscountSet)
class DiscountSetAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "percentage", "start_date", "end_date"
    list_display_links = ("pk",)


@admin.register(DiscountProduct)
class DiscountProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "percentage", "start_date", "end_date"
    list_display_links = ("pk",)


@admin.register(DiscountCart)
class DiscountCartAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "percentage", "start_date", "end_date"
    list_display_links = ("pk",)
