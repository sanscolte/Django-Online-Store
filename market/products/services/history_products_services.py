from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from products.models import Product, HistoryProducts

User = get_user_model()


class HistoryProductsService:
    """Сервис для работы с историей просмотров продуктов"""

    def __init__(self, product: Product, user: User):
        self.product = product
        self.user = user

    def add_product_history(self) -> None:
        """Добавляет товар к списку просмотренных товаров"""

        if self.check_product_in_history():
            history_last_obj = HistoryProducts.objects.last().product

            if self.product == history_last_obj:
                return
            else:
                self.delete_product_from_history()

                HistoryProducts.objects.create(
                    product=self.product,
                    user=self.user,
                )
        else:
            HistoryProducts.objects.create(
                product=self.product,
                user=self.user,
            )

    def delete_product_from_history(self) -> None:
        """Удаляет товар из списка просмотренных товаров"""

        HistoryProducts.objects.get(product=self.product).delete()

    def check_product_in_history(self) -> bool:
        """
        Узнать, есть ли товар уже в списке просмотренных товаров
        :return: флаг
        """

        if HistoryProducts.objects.filter(product=self.product):
            return True
        return False

    def get_history(self, count: int = 20) -> QuerySet[HistoryProducts]:
        """
        Получить список просмотренных товаров
        :param count: необязательный параметр, сколько последних товаров возвратить
        :return: список просмотренных товаров
        """

        history = HistoryProducts.objects.filter().order_by("-pk")[:count]
        return history

    def get_history_count(self) -> int:
        """
        Получить количество просмотренных товаров
        :return: число просмотренных товаров
        """
        history_count = HistoryProducts.objects.all().count()
        return history_count
