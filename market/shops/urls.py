from django.urls import path
from .views import ShopPageView, CatalogPageView


app_name = "shops"


urlpatterns = [
    path("", ShopPageView.as_view(), name="home"),
    path("catalog/", CatalogPageView.as_view(), name="catalog"),
]
