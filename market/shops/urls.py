from django.urls import path
from .views import ShopPageView


app_name = "shops"


urlpatterns = [
    path("", ShopPageView.as_view(), name="shops"),
]
