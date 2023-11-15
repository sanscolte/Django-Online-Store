from django.urls import path
from .views import (
    ShopPageView,
    ShopDetailView,
)

app_name = "shops"


urlpatterns = [
    path("", ShopPageView.as_view(), name="shops"),
    path("shops/<int:pk>/", ShopDetailView.as_view(), name="shops_detail"),
]
