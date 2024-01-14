from django.urls import path
from .views import DiscountListView, DiscountProductDetailView, DiscountSetDetailView, DiscountCartDetailView

app_name = "discounts"


urlpatterns = [
    path("", DiscountListView.as_view(), name="discount-list"),
    path("product/<int:pk>/", DiscountProductDetailView.as_view(), name="discount-product"),
    path("set/<int:pk>/", DiscountSetDetailView.as_view(), name="discount-set"),
    path("cart/<int:pk>/", DiscountCartDetailView.as_view(), name="discount-cart"),
]
