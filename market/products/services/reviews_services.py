from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import QuerySet
from django.http import HttpRequest

from products.models import Product, Review

User = get_user_model()


class ReviewsService:
    """Сервис для работы с отзывами"""

    def __init__(self, request: HttpRequest, user: User, product: Product):
        self.request = request
        self.user = user
        self.product = product

    def add(self, review_text: str) -> None:
        """
        Добавляет отзыв к товару
        :param review_text: текст отзыва о товаре
        :return: None
        """

        Review.objects.create(
            product=self.product,
            user=self.user,
            text=review_text,
        )

    def get_reviews_for_product(self) -> QuerySet[Review]:
        """
        Возвращает отзывы о выбранном товаре
        :return: пагинатор
        """

        reviews = Review.objects.filter(product=self.product)
        paginator = Paginator(reviews, 2)
        page = self.request.GET.get("page")

        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)

        return reviews

    def get_reviews_count(self) -> int:
        """
        Возвращает количество отзывов о выбранном товаре
        :return: число отзывов
        """

        reviews_count = Review.objects.filter(product=self.product).count()
        return reviews_count
