from django.urls import path

from .views import (
    MyLoginView,
    MyLogoutView,
    MyAccountView,
    MyRegisterView,
    ProfileView,
    MyPasswordResetView,
    MyPasswordResetConfirmView,
    MyPasswordResetDoneView,
    MyPasswordResetCompleteView,
)
from config import settings
from django.conf.urls.static import static


app_name = "accounts"


urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("my-account/", MyAccountView.as_view(), name="my-account"),
    path("registration/", MyRegisterView.as_view(), name="registration"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password-reset/", MyPasswordResetView.as_view(), name="password_reset"),
    path("password-reset-done/", MyPasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        MyPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password-reset/complete/", MyPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
