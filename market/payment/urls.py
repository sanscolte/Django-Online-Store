from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payment.views import (
    PaymentWithCardView,
    ProgressPaymentView,
    BankTransactionViewSet,
)

app_name = "payment"

routers = DefaultRouter()
routers.register(r"banktransactions", BankTransactionViewSet)

urlpatterns = [
    path("api/", include(routers.urls)),
    path("with-card/", PaymentWithCardView.as_view(), name="payment_with_card"),
    path("progress/", ProgressPaymentView.as_view(), name="progress_payment"),
]
