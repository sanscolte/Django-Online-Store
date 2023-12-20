from django.contrib import admin

from discounts.models import DiscountSet, DiscountProduct


@admin.register(DiscountSet)
class DiscountSetAdmin(admin.ModelAdmin):
    list_display = "pk", "percentage", "start_date", "end_date"
    list_display_links = ("pk",)


@admin.register(DiscountProduct)
class DiscountProductAdmin(admin.ModelAdmin):
    list_display = "pk", "percentage", "start_date", "end_date"
    list_display_links = ("pk",)
