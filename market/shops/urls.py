from django.urls import path

from .views import ProductListView, ShopPageView, ShopDetailView

app_name = "shops"


urlpatterns = [
    path("", ShopPageView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="products"),
    path("shops/<int:pk>/", ShopDetailView.as_view(), name="shops_detail"),
]
