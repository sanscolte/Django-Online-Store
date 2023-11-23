from django.apps import AppConfig
from .models import post_save_product, post_delete_product
from django.db.models.signals import post_save, post_delete
from .models import Product


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        post_save.connect(post_save_product, sender=Product)
        post_delete.connect(post_delete_product, sender=Product)
