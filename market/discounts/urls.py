from django.urls import path
from .views import DiscountTemplateView

app_name = "discounts"


urlpatterns = [
    path("", DiscountTemplateView.as_view(), name="discount-list"),
]
