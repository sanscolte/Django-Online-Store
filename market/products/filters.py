from django_filters import FilterSet
from .models import Product


class F(FilterSet):
    class Meta:
        model = Product
        fields = ["name", "offers"]
