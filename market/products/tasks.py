import json
import logging
import os
import shutil
import ssl

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.mail import send_mail
from django.utils import timezone

from products.models import Product, Category
from shops.models import Shop, Offer

from products.models import ProductImport

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
def import_products(file_ids: list[id], email: str = None):  # noqa
    set_import_status("В процессе выполнения")

    for file_id in file_ids:
        file_obj = ProductImport.objects.get(id=file_id)
        file_path = file_obj.file.path

        success_location = os.path.join(settings.MEDIA_ROOT, "import/success/")
        fail_location = os.path.join(settings.MEDIA_ROOT, "import/fail/")

        with open(file_path, encoding="utf-8") as fp:
            data = json.load(fp)

        # заранее объявляем поля
        product_name = "None"
        product_description = "None"
        category = "None"
        shop_name = "None"
        shop_description = "None"
        phone = "None"
        address = "None"
        shop_email = "None"
        offer_shop = "None"
        offer_product = "None"
        offer_price = "None"
        remains = "None"
        is_success = True
        is_created = "Не создан"

        # переопределяем поля
        for obj in data:
            # обязательные поля
            try:
                product_name = obj["Товар"]
                category = obj["Категория товара"]
                shop_name = obj["Магазин"]
                phone = obj["Телефон"]
                address = obj["Адрес"]
                shop_email = obj["Email"]
                offer_shop = obj["Магазин оффера"]
                offer_product = obj["Продукт оффера"]
                offer_price = obj["Цена оффера"]
                remains = obj["Остатки"]
            except KeyError:
                is_success = False

            # необязательные поля
            try:
                product_description = obj["Описание товара"]
                shop_description = obj["Описание магазина"]
            except KeyError:
                pass

            if is_success:
                message: str = (
                    f"Были успешно импортированы продукты от {shop_name}: {product_name}, "
                    f'{timezone.now().strftime("%d-%b-%y %H:%M:%S")}'
                )

                # Создаем экземпляры моделей
                created_category = Category.objects.get_or_create(name=category)[0]
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
                offer = Offer.objects.get_or_create(
                    shop=created_shop,
                    product=created_product,
                    price=offer_price,
                    remains=remains,
                )[1]
                created_shop.products.add(created_product)

                if offer is True:
                    set_import_status("Выполнен")
                    is_created: str = "Создан"
                else:
                    set_import_status("Завершён с ошибкой")

            else:
                set_import_status("Завершён с ошибкой")
                message: str = (
                    f"Были неуспешно импортированы продукты от {shop_name}: {product_name}, "
                    f'{timezone.now().strftime("%d-%b-%y %H:%M:%S")}'
                )

            # Отправляем электронное письмо
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

            # Логируем запись в файл
            logger.debug(
                "",
                extra={
                    "is_success": is_created,
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

        # Перемещаем файл в нужную директории в зависимости от успешности импорта
        if is_created == "Создан":
            shutil.move(file_path, success_location)
        else:
            shutil.move(file_path, fail_location)


def get_import_status():
    """Функция получения статуса импорта"""
    status = cache.get("import_status")
    if status:
        return status
    else:
        set_import_status("Импорт не начался")
        status = cache.get("import_status")
        return status


def set_import_status(status):
    """Функция установки статуса импорта"""
    cache.set("import_status", status)
