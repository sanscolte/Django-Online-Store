from django.urls import path

from .views import (
    OrderStepOneView,
    OrderStepTwoView,
    OrderStepThreeView,
)

app_name = "orders"

urlpatterns = [
    path("step_1/", OrderStepOneView.as_view(), name="order_step_1"),
    path("step_2/", OrderStepTwoView.as_view(), name="order_step_2"),
    path("step_3/", OrderStepThreeView.as_view(), name="order_step_3"),
]
