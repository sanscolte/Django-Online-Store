import json
import logging
import os
import shutil

from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils import timezone
from pydantic import BaseModel, Field

from products.models import Product, Category
from products.utils import send_email
from shops.models import Shop, Offer

from products.models import ProductImport

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join("logs/import/products-import.log"))
formatter = logging.Formatter(
    "%(asctime)s - %(is_success)s - %(product_name)s - %(category)s - %(shop_name)s - %(phone)s - "
    "%(address)s - %(shop_email)s - %(offer_shop)s - %(offer_product)s - %(offer_price)s - %(remains)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

logger.addHandler(file_handler)
file_handler.setFormatter(formatter)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class ProductImportFile(BaseModel):
    """Класс, заранее объявляющий необходимые поля для файла импорта"""

    product_name: str = Field("None", alias="Товар")
    product_description: str = Field("None", alias="Описание товара")
    category: str = Field("None", alias="Категория товара")
    shop_name: str = Field("None", alias="Магазин")
    shop_description: str = Field("None", alias="Описание магазина")
    phone: str = Field("None", alias="Телефон")
    address: str = Field("None", alias="Адрес")
    shop_email: str = Field("None", alias="Email")
    offer_shop: str = Field("None", alias="Магазин оффера")
    offer_product: str = Field("None", alias="Продукт оффера")
    offer_price: int = Field("None", alias="Цена оффера")
    remains: int = Field("None", alias="Остатки")

    class Config:
        """Параметр позволяющий использовать alias как ключ"""

        populate_by_name = True

    @property
    def is_success(self) -> bool:
        """Метод возвращает флаг, указывающий на то, все ли поля были указаны явно"""
        fields_set = self.__fields_set__
        all_fields = set(self.__fields__.keys())
        return fields_set == all_fields


@shared_task
def import_products(file_ids: list[id], email: str = None) -> None:  # noqa
    set_import_status("В процессе выполнения")
    message = ""

    for file_id in file_ids:
        file_obj = ProductImport.objects.get(id=file_id)
        file_path = file_obj.file.path

        success_location = os.path.join(settings.MEDIA_ROOT, "import/success/")
        fail_location = os.path.join(settings.MEDIA_ROOT, "import/fail/")

        with open(file_path, encoding="utf-8") as fp:
            data = json.load(fp)

        is_success = True
        is_created = "Не создан"

        for obj in data:
            pif = ProductImportFile(**obj)

            if not pif.is_success:
                is_success = False

            if is_success:
                message += (
                    f'Успешный импорт продуктов {timezone.now().strftime("%d-%b-%y %H:%M:%S")} от {pif.shop_name}\n'
                )

                created_category = Category.objects.get_or_create(name=pif.category)[0]
                created_shop = Shop.objects.get_or_create(
                    name=pif.shop_name,
                    description=pif.shop_description,
                    phone=pif.phone,
                    address=pif.address,
                    email=pif.shop_email,
                )[0]
                created_product, _ = Product.objects.get_or_create(
                    name=pif.product_name,
                    category=created_category,
                    description=pif.product_description,
                )
                offer = Offer.objects.get_or_create(
                    shop=created_shop,
                    product=created_product,
                    price=pif.offer_price,
                    remains=pif.remains,
                )[1]
                created_shop.products.add(created_product)

                if offer is True:
                    set_import_status("Выполнен")
                    is_created: str = "Создан"
                else:
                    set_import_status("Завершён с ошибкой")

            else:
                set_import_status("Завершён с ошибкой")
                message += (
                    f'Неуспешный импорт продуктов {timezone.now().strftime("%d-%b-%y %H:%M:%S")} от {pif.shop_name}\n'
                )

            log_data = pif.model_dump(exclude={"product_description", "shop_description"})
            log_data["is_success"] = is_created
            logger.debug("", extra=log_data)

        if is_created == "Создан":
            shutil.move(file_path, success_location)
        else:
            shutil.move(file_path, fail_location)

    if email:
        send_email(email, message)


def get_import_status() -> str:
    """Функция получения статуса импорта"""
    status = cache.get("import_status")
    if status:
        return status
    else:
        set_import_status("Импорт не начался")
        status = cache.get("import_status")
        return status


def set_import_status(status: str) -> None:
    """Функция установки статуса импорта"""
    cache.set("import_status", status, timeout=settings.CACHE_TTL)
