from django.urls import path

from payment.views import PaymentWithCardView, ProgressPaymentView

app_name = "payment"

urlpatterns = [
    path("with-card/", PaymentWithCardView.as_view(), name="payment_with_card"),
    path("progress/", ProgressPaymentView.as_view(), name="progress_payment"),
]
