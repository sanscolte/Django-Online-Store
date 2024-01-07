from django.urls import path

from .views import OrderStepOneView

app_name = "orders"

urlpatterns = [
    path("step_1/", OrderStepOneView.as_view(), name="order_step_1"),
]
