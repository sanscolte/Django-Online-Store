from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from products.models import Product, ProductsViews

User = get_user_model()


class ProductsViewsService:
    """Сервис для работы с историей просмотров продуктов"""

    def __init__(self, product: Product, user: User) -> None:
        self.product = product
        self.user = user

    def add_product_view(self) -> None:
        """Добавляет товар в список просмотренных товаров"""

        if self.check_product_in_views():
            views_last_obj = ProductsViews.objects.first().product
            if self.product == views_last_obj:
                return
            else:
                self.delete_product_from_views()
                self.create_product_view()
        else:
            self.create_product_view()

    def delete_product_from_views(self) -> None:
        """Удаляет товар из списка просмотренных товаров"""

        ProductsViews.objects.get(product=self.product).delete()

    def check_product_in_views(self) -> bool:
        """
        Узнать, есть ли товар уже в списке просмотренных товаров
        :return: флаг
        """

        if ProductsViews.objects.filter(product=self.product):
            return True
        return False

    def get_views(self, count: int = 20) -> QuerySet[ProductsViews]:
        """
        Получить список просмотренных товаров
        :param count: необязательный параметр, сколько последних товаров возвратить
        :return: список просмотренных товаров
        """

        views = ProductsViews.objects.filter().order_by("-pk")[:count]
        return views

    def get_views_count(self) -> int:
        """
        Получить количество просмотренных товаров
        :return: число просмотренных товаров
        """
        views_count = ProductsViews.objects.all().count()
        return views_count

    def create_product_view(self) -> None:
        """Создать объект просмотра товара"""
        ProductsViews.objects.create(
            product=self.product,
            user=self.user,
        )
