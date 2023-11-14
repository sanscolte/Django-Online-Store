from django.contrib import admin  # noqa F401

from products.models import Banner, Product


class DetailsInline(admin.TabularInline):
    model = Product.details.through


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = "product", "image", "is_active"
    list_display_links = ("product",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        DetailsInline,
    ]
    list_display = ("name",)
    list_display_links = ("name",)
