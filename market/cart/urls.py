from django.urls import path
from cart.views import CartDetail, cart_add, cart_remove

app_name = "cart"

urlpatterns = [
    path("", CartDetail.as_view(), name="cart_detail"),
    path("add/<int:pk>/", cart_add, name="cart_add"),
    path("remove/<int:pk>/", cart_remove, name="cart_remove"),
]
