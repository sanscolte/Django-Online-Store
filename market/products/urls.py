from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductsViewsView,
    ComparisonListView,
    AddToComparisonListView,
    RemoveFromComparisonListView,
)

app_name = "products"


urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/add-to-list", AddToComparisonListView.as_view(), name="add-to-list"),
    path("<int:pk>/remove-from-list", RemoveFromComparisonListView.as_view(), name="remove-from-list"),
    path("history/", ProductsViewsView.as_view(), name="products-history"),
    path("list/", ComparisonListView.as_view(), name="comparison-list"),
]
