from django.db.models import Avg
from django.db.models.functions import Round
from django_filters import FilterSet
from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        queryset = Product.objects.annotate(avg_price=Round(Avg("offers__price"), 2))
        fields = {
            "avg_price": ["lte", "gte"],
            "name": ["icontains"],
        }
