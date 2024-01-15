import logging
import os.path
import time  # noqa

from django.contrib import admin  # noqa F401
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import path

from .forms import ProductImportForm
from .models import (
    Category,
    Product,
    Banner,
    Review,
    ProductImage,
    ProductDetail,
    Detail,
    ProductsViews,
    ProductImport,
)  # noqa
from .tasks import import_products, get_import_status  # noqa

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join("logs/import/products-import.log"))
formatter = logging.Formatter("%(asctime)s - %(product)s - %(category)s - %(is_success)s", datefmt="%d-%b-%y %H:%M:%S")

logger.addHandler(file_handler)
file_handler.setFormatter(formatter)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "is_active"
    list_display_links = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "name", "description_short", "date_of_publication", "category_id"
    list_display_links = ("name",)
    change_list_template = "products/products_changelist.html"

    def import_json(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = ProductImportForm()
            status = get_import_status()
            # if status == "В процессе выполнения":
            #     context = {
            #         "status": "Предыдущий импорт ещё не выполнен. Пожалуйста, дождитесь его окончания",
            #     }
            #     return render(request, "admin/product-import-form.html", context)

            context = {
                "form": form,
                "status": status,
            }
            return render(request, "admin/product-import-form.html", context)

        if request.method == "POST":
            success_message = "Продукты успешно импортированы"
            error_message = "Ошибка при импорте продуктов"
            start_message = "Импорт начался"

            form = ProductImportForm(request.POST, request.FILES)
            # files_objs = []

            if form.is_valid():
                files = form.cleaned_data["json_files"]
                email = form.cleaned_data["email"]  # noqa

                # for file in files:
                files_obj = ProductImport.objects.create(file=files)
                # files_objs.append(file_obj)

                import_products.delay(files_obj=files_obj, email=email)

            status = get_import_status()
            context = {
                "form": form,
                "status": status,
            }

            if status == "Выполнен":
                self.message_user(request, success_message)
            if status == "Завершён с ошибкой":
                self.message_user(request, error_message)
            else:
                self.message_user(request, start_message)

            return render(request, "admin/product-import-form.html", context)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("import-products/", self.import_json, name="import_products")]
        return new_urls + urls


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = "product", "image", "is_active"
    list_display_links = ("product",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "product", "text", "user", "created_at"
    list_display_links = "product", "text", "user"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = "product", "image", "sort_image"


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = "product", "detail", "value"
    list_display_links = ("detail",)


@admin.register(ProductsViews)
class ProductsViewsAdmin(admin.ModelAdmin):
    list_display = "product", "user", "created_at"
    list_display_links = "product", "user"
