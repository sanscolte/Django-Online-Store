from django.urls import path
from .views import ShopPageView, ProductListView


app_name = "shops"


urlpatterns = [
    path("", ShopPageView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="products"),
]
