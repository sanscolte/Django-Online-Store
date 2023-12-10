from decimal import Decimal
from django.db.models import Avg, QuerySet, Count
from django.db.models.functions import Round
from django_filters import FilterSet, NumberFilter, OrderingFilter

from .models import Product


class ProductFilter(FilterSet):
    avg_price__gte = NumberFilter(
        method="avg_price__gte_filter",
        help_text="Фильтр по минимальной средней цене товара.",
    )

    avg_price__lte = NumberFilter(
        method="avg_price__lte_filter",
        help_text="Фильтр по максимальной средней цене товара.",
    )

    reviews__lte = NumberFilter(method="reviews__lte_filter", help_text="Фильтр по минимальному количеству на товар")

    reviews__gte = NumberFilter(method="reviews__gte_filter", help_text="Фильтр по максимальному количеству на товар")

    o = OrderingFilter(
        # https://django-filter.readthedocs.io/en/stable/ref/filters.html#orderingfilter
        fields=(
            ("date_of_publication", "publication"),
            ("avg_price", "avg_price"),
            ("reviews_count", "reviews_count"),
        ),
    )

    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
        }

    def avg_price__gte_filter(self, queryset: QuerySet[Product], _: str, value: Decimal) -> QuerySet[Product]:
        """Фильтрация по минимальной средней цене товара."""
        queryset = self._annotate_avg_price(queryset)
        return queryset.filter(
            avg_price__gte=value,
        )

    def avg_price__lte_filter(self, queryset: QuerySet[Product], _: str, value: Decimal) -> QuerySet[Product]:
        """Фильтрация по максимальной средней цене товара."""
        queryset = self._annotate_avg_price(queryset)
        return queryset.filter(
            avg_price__lte=value,
        )

    def reviews_count__lte_filter(self, queryset, _, value):
        """Фильтрация по максимальному количеству отзывов на товар"""
        queryset = self._annotate_reviews(queryset)
        return queryset.filter(
            avg_price__lte=value,
        )

    def reviews_count__gte_filter(self, queryset, _, value):
        """Фильтрация по минимальному количеству отзывов на товар"""
        queryset = self._annotate_reviews(queryset)
        return queryset.filter(
            avg_price__lte=value,
        )

    @staticmethod
    def _annotate_avg_price(queryset: QuerySet[Product]) -> QuerySet[Product]:
        return queryset.annotate(avg_price=Round(Avg("offers__price"), 2))

    @staticmethod
    def _annotate_reviews(queryset: QuerySet[Product]) -> QuerySet[Product]:
        return queryset.annotate(reviews_count=Count("reviews"))
