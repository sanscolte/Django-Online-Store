import json
import logging
import os
import ssl

from celery import shared_task
from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.mail import send_mail
from django.utils import timezone

from products.models import Product, Category
from shops.models import Shop, Offer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join("logs/import/products-import.log"))
formatter = logging.Formatter(
    "%(asctime)s - %(is_success)s - %(product)s - %(category)s - %(shop)s - %(phone)s - "
    "%(address)s - %(email)s - %(offer_shop)s - %(offer_product)s - %(offer_price)s - %(remains)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

logger.addHandler(file_handler)
file_handler.setFormatter(formatter)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


@shared_task
def import_products(filename, is_valid, email):  # noqa
    if is_valid:
        location = os.path.join(settings.MEDIA_ROOT, f"import/success/{filename}")
    else:
        location = os.path.join(settings.MEDIA_ROOT, f"import/fail/{filename}")

    with open(location) as json_file:
        json_file = json_file.read()

    try:
        data = json.loads(json_file)
    except json.decoder.JSONDecodeError:
        raise forms.ValidationError("Ошибка при чтении файла JSON")

    for obj in data:
        # продукт
        try:
            product_name = obj["Товар"]
        except KeyError:
            product_name = None
        try:
            product_description = obj["Описание товара"]
        except KeyError:
            product_description = "None"
        try:
            category = obj["Категория товара"]
        except KeyError:
            category = "None"

        # магазин
        try:
            shop_name = obj["Магазин"]
        except KeyError:
            shop_name = "None"
        try:
            shop_description = obj["Описание магазина"]
        except KeyError:
            shop_description = "None"
        try:
            phone = obj["Телефон"]
        except KeyError:
            phone = "None"
        try:
            address = obj["Адрес"]
        except KeyError:
            address = "None"
        try:
            shop_email = obj["Email"]
        except KeyError:
            shop_email = "None"

        # оффер
        try:
            offer_shop = obj["Магазин оффера"]
        except KeyError:
            offer_shop = "None"
        try:
            offer_product = obj["Продукт оффера"]
        except KeyError:
            offer_product = "None"
        try:
            offer_price = obj["Цена оффера"]
        except KeyError:
            offer_price = "None"
        try:
            remains = obj["Остатки"]
        except KeyError:
            remains = "None"

        if is_valid:
            is_success = "SUCCESS"
            message = (
                f"Были успешно импортированы продукты от {shop_name}: {product_name}, "
                f'{timezone.now().strftime("%d-%b-%y %H:%M:%S")}'
            )

        else:
            is_success = "FAIL"
            message = (
                f"Были неуспешно импортированы продукты от {shop_name}: {product_name}, "
                f'{timezone.now().strftime("%d-%b-%y %H:%M:%S")}'
            )

        logger.debug(
            "",
            extra={
                "is_success": is_success,
                "product": product_name,
                "category": category,
                "shop": shop_name,
                "phone": phone,
                "address": address,
                "email": email,
                "offer_shop": offer_shop,
                "offer_product": offer_product,
                "offer_price": offer_price,
                "remains": remains,
            },
        )

        if is_success == "SUCCESS":
            created_category = Category.objects.get(name=category)
            created_shop = Shop.objects.get_or_create(
                name=shop_name,
                description=shop_description,
                phone=phone,
                address=address,
                email=shop_email,
            )[0]
            created_product, _ = Product.objects.get_or_create(
                name=product_name,
                category=created_category,
                description=product_description,
            )
            Offer.objects.create(
                shop=created_shop,
                product=created_product,
                price=offer_price,
                remains=remains,
            )
            created_shop.products.add(created_product)

        try:
            send_mail(
                subject="Импорт продуктов",
                message=message,
                recipient_list=[email],
                from_email=settings.DEFAULT_FROM_EMAIL,
                fail_silently=False,
            )
        except ssl.SSLCertVerificationError:
            pass

    return "Import completed"


def get_import_status():
    status = cache.get("import_status")
    if status:
        return status
    else:
        set_import_status("Импорт не начался")
        status = cache.get("import_status")
        return status


def set_import_status(status):
    cache.set("import_status", status)
