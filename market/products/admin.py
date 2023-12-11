from django.contrib import admin  # noqa F401

from .models import Category, Product, Banner, Review, ProductImage, HistoryProducts


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "is_active"
    list_display_links = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "date_of_publication", "category_id"
    list_display_links = ("name",)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = "product", "image", "is_active"
    list_display_links = ("product",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "product", "text", "user"
    list_display_links = "product", "text", "user"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "product", "image", "sort_image"


@admin.register(HistoryProducts)
class HistoryProductsAdmin(admin.ModelAdmin):
    list_display = "product", "user"
    list_display_links = "product", "user"
