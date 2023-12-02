from decimal import Decimal
from django.db.models import Avg, QuerySet
from django.db.models.functions import Round
from django_filters import FilterSet, NumberFilter

from .models import Product


class ProductFilter(FilterSet):
    avg_price__gte = NumberFilter(
        method="avg_price__gte_filter",
        # coerce=Decimal,
        help_text="...",
    )

    avg_price__lte = NumberFilter(
        method="avg_price__lte_filter",
        # coerce=Decimal,
        help_text="...",
    )

    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
        }

    def avg_price__gte_filter(self, queryset: QuerySet[Product], _: str, value: Decimal) -> QuerySet[Product]:
        """Фильтрация по типу документа."""
        queryset = self._annotate_avg_price(queryset)
        return queryset.filter(
            avg_price__gte=value,
        )

    def avg_price__lte_filter(self, queryset: QuerySet[Product], _: str, value: Decimal) -> QuerySet[Product]:
        """Фильтрация по типу документа."""
        queryset = self._annotate_avg_price(queryset)
        return queryset.filter(
            avg_price__lte=value,
        )

    @staticmethod
    def _annotate_avg_price(queryset: QuerySet[Product]) -> QuerySet[Product]:
        return queryset.annotate(avg_price=Round(Avg("offers__price"), 2))
