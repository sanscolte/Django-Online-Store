from django.urls import path
from .views import ProductListView, ProductDetailView, HistoryProductsView

app_name = "products"


urlpatterns = [
    path("", ProductListView.as_view(), name="products"),
    path("<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("history", HistoryProductsView.as_view(), name="products-history"),
]
