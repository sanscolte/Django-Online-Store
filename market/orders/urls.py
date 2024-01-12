from django.urls import path

from .views import (
    OrderStepOneView,
    OrderStepTwoView,
    OrderStepThreeView,
    OrderStepFourView,
)

app_name = "orders"

urlpatterns = [
    path("step_1/", OrderStepOneView.as_view(), name="order-step-1"),
    path("step_2/", OrderStepTwoView.as_view(), name="order-step-2"),
    path("step_3/", OrderStepThreeView.as_view(), name="order-step-3"),
    path("step_4/", OrderStepFourView.as_view(), name="order-step-4"),
]
