from django.urls import path

from .views import IndexPageView, ShopDetailView


app_name = "shops"


urlpatterns = [
    path("", IndexPageView.as_view(), name="home"),
    path("shops/<int:pk>/", ShopDetailView.as_view(), name="shops_detail"),
]
