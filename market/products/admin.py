import json
import logging
import os.path

from django.contrib import admin  # noqa F401
from django.core.files.storage import FileSystemStorage
from django.core.management import call_command
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import path

from .forms import ProductImportForm
from .models import Category, Product, Banner, Review, ProductImage, ProductDetail, Detail, ProductsViews

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join("logs/import/products-import.log"))
formatter = logging.Formatter("%(asctime)s - %(product)s - %(category)d - %(is_success)s", datefmt="%d-%b-%y %H:%M:%S")

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
            context = {
                "form": form,
            }
            return render(request, "admin/product-import-form.html", context)

        form = ProductImportForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/product-import-form.html", context, status=400)

        file = form.cleaned_data["json_file"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        call_command("loaddata", file.name)

        print("saved file", filename)
        self.message_user(request, "Data from file was imported")

        with open(os.path.join(f"uploads/{filename}"), "r") as json_file:
            json_file = json_file.read()
            data = json.loads(json_file)

        for product in data:
            product_name = product["fields"]["name"]
            category = product["fields"]["category"]
            is_success = "SUCCESS"
            logger.debug("", extra={"product": product_name, "category": category, "is_success": is_success})

        return redirect("..")

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
